from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from functools import wraps
from django.core.exceptions import PermissionDenied
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.db.models import Max
from django.core.mail import EmailMessage, get_connection
from accounts.models import EmailConfiguration

def custom_paginate(model, page=1, per_page=10, filters=None):
    """
    Paginate any Django model.

    :param model: Django model class
    :param page: Current page number (default: 1)
    :param per_page: Items per page (default: 10)
    :param filters: Optional dictionary to filter queryset
    :return: Dictionary with paginated results
    """
    if filters:
        queryset = model.objects.filter(**filters)
    else:
        queryset = model.objects.all()
    
    paginator = Paginator(queryset, per_page)

    try:
        paginated_data = paginator.page(page)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)

    return {
        'items': paginated_data.object_list,
        'current_page': paginated_data.number,
        'total_pages': paginator.num_pages,
        'total_items': paginator.count,
        'has_next': paginated_data.has_next(),
        'has_previous': paginated_data.has_previous(),
    }
    
def get_last_six_or_pad(value):
    value = str(value)  # make sure it's a string
    if len(value) >= 6:
        return value[-6:]
    else:
        return value.zfill(6)   # pads with zeros on the left    

def generate_auto_id(model_class,number=4,insurer=False):
    year_prefix = datetime.now().strftime('%y')
    last_record = model_class.objects.order_by('-id').first()
    if last_record:
        new_number = int(last_record.id) + 1
        last_digits = str(new_number).zfill(3)
    else:
        last_digits = '001'  # default if no record or no auto_id
        if number> 3:
            last_digits = '0001'
    if insurer:
        new_auto_id = f"{year_prefix}{'i-'}{last_digits}"
    else:
        new_auto_id = f"{year_prefix}{last_digits}"
    return new_auto_id

def get_martial_status(value):
    if not value:
        return "S"  
    if value in ["Married", "Merried", "married","Merried","M",'m']:
        return "M"
    elif value in ["Divorced", "divorced", "d","D"]:
        return "D"
    elif value in ["Widowed", "widowed", "w","D"]:
        return "W"
    else:
        return "S"  
    
def get_bank_account_type_status(value):
    if not value:
        return "mfs"  
    if value in ["Bank", "bank",'b']:
        return "bank"
    elif value in ["Mobile Financial Service", "mobile financial fervice", "MFS","mfs",'MFC']:
        return "mfs"
    else:
        return "mfs"  
    
def get_sex_status(value):
    if not value:
        return "male"  
    if value in ["Male", "male",'M','m']:
        return "male"
    elif value in ["Female", "female", "f","F"]:
        return "female"
    elif value in ["Other", "other", "O","o"]:
        return "other"
    else:
        return "male"     
    
def get_relation_status(value):
    if not value:
        return "self"  
    if value in ["Self", "self",'s','S']:
        return "self"
    elif value in ["Father", "father", "f","F"]:
        return "father"
    elif value in ["Mother", "mother", "M","m"]:
        return "mother"
    elif value in ["Child", "child", "c","C"]:
        return "child"
    elif value in ["Sister", "sister"]:
        return "sister"
    elif value in ["Wife", "wife"]:
        return "wife"
    elif value in ["Wife", "wife"]:
        return "wife"
    elif value in ["husband", "Husband"]:
        return "husband"
    else:
        return "self"

def get_yes_no_status(value):
    if not value:
        return "n"  
    if value in ["Yes","YES", "yes",'Y','y']:
        return "y"
    else:
        return "n"

def permission_required_or_superuser_with_token(perm):
    """
    Decorator that:
    - Allows superuser
    - Checks permission for normal user
    - Supports DRF TokenAuthentication
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = None

            # First check if user is authenticated normally
            if request.user and request.user.is_authenticated:
                user = request.user
            else:
                # Try token auth for API
                auth = TokenAuthentication()
                try:
                    user_auth_tuple = auth.authenticate(request)
                    if user_auth_tuple:
                        user, _ = user_auth_tuple
                except AuthenticationFailed:
                    pass

            if not user:
                raise PermissionDenied("Authentication required.")

            if user.is_superuser or user.has_perm(perm):
                request.user = user
                return view_func(request, *args, **kwargs)

            raise PermissionDenied(f"You do not have permission: {perm}")

        return _wrapped_view
    return decorator




def group_required_multiple(*group_names):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.is_superuser or user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            return redirect('no_permission')
        return _wrapped_view
    return decorator


from django.core.mail import EmailMessage, get_connection
from django.contrib.auth.models import Group
from django.conf import settings
from accounts.models import EmailConfiguration, EmailTemplate


def send_dynamic_email(to_email, template_type, group=None, user=None, context=None):
    """
    Sends an email using dynamic configuration and template.
    :param to_email: recipient email address (string or list)
    :param template_type: 'group' or 'user'
    :param group: Group instance (if group type)
    :param user: User instance (if user type)
    :param context: dict for message placeholders (optional)
    """
    # 1. Get the active email configuration
    config = EmailConfiguration.objects.filter(is_active=True).first()
    if not config:
        raise ValueError("No active email configuration found.")
    # 2. Pick the appropriate template
    if template_type == "group" and group:
        template = EmailTemplate.objects.filter(
            template_type="group", group=group, is_active=True,status=context.get("status")
        ).first()
    elif template_type == "user" and user:
        template = EmailTemplate.objects.filter(
            template_type="user", user=user, is_active=True,status=context.get("status")
        ).first()
    else:
        raise ValueError("Invalid template type or missing group/user.")

    if not template:
        return "Email template not set"

    subject = template.subject
    message = template.message

    # Optional: format the message with context variables
    if context:
        try:
            message = message.format(**context)
        except KeyError as e:
            print(f"Missing context key: {e}")

    # 3. Set up the SMTP connection dynamically
    connection = get_connection(
        host=config.host,
        port=config.port,
        username=config.host_user,
        password=config.host_password,
        use_tls=config.use_tls,
        use_ssl=config.use_ssl,
    )

    # 4. Create and send the email
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=config.host_user,
        to=[to_email] if isinstance(to_email, str) else to_email,
        connection=connection,
    )

    email.send(fail_silently=False)
    return f"Email sent to {to_email} using template '{template}'"
