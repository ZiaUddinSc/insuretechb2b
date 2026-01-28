import json
import os
from django.conf import settings
from django.contrib.auth.models import Group
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import TemplateHTMLRenderer,JSONOpenAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import login,logout
from knox.models import AuthToken
from rest_framework.authtoken.models import Token
from django.db.models import Q
from core.utils import group_required_multiple
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.http import HttpResponse
from .models import CustomUser,EmailTemplate,EmailConfiguration,EditLog
from .serializers import EditLogSerializer,GroupSerializer, UserCreateSerializer,CustomUserRegisterSerializer,CustomUserSerializer,EmailConfigurationListSerializer,EmailTemplateListSerializer,CustomUserListSerializer
from rest_framework.permissions import IsAdminUser
from datetime import datetime
from django.core.management import call_command
# Create your views here.

def userLogin(request):
    # users = User.objects.all()
    template_name = 'accounts/login.html'
    return render(request,template_name=template_name)

"""Customer User login using phone username or email"""

class CustomUserLoginAPIView(APIView):
    
    renderer_classes=[JSONOpenAPIRenderer,TemplateHTMLRenderer]
    template_name = 'accounts/login.html'
    permission_classes = [AllowAny]  # Allow anyone to access this view

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to render the login page.
        """
        # print('authenticate',request.user)
      
        # queryset = CustomUser.objects.all()
        # serializer = CustomUserSerializer(queryset)
        # print('serria',serializer.data)
        # return Response({'data':serializer.data},template_name=self.template_name)
        return render(request, template_name=self.template_name)
        
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        # print('post',username,password)
        try:
            user = CustomUser.objects.get(
                Q(email=username) 
            )
            if not user.is_active:
                messages.error(request, 'Email has been deactivated')
                return render(request, 'accounts/login.html')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Email does not exist')
            return render(request, 'accounts/login.html')
        if not username or not password:
            return Response({'error': 'Email or Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        # print('user',user)
        if user is not None:
            login(request, user)
            _, token = AuthToken.objects.create(user)
            # Redirect to group-based dashboard
            if user.is_superuser is not True:
                if user.groups.filter(name='Organization HR').exists():
                    response = redirect('hr_admin_dashboard')
                elif user.groups.filter(name='Shield Operation').exists():
                    response = redirect('waadaa_operation_dashboard')
                elif user.groups.filter(name='B2B Employee').exists():
                    response = redirect('b2b_employee_dashboard')
                elif user.groups.filter(name='Insurer Claim Officer').exists():
                    response = redirect('insurer_claim_dashboard')
                elif user.groups.filter(name='Claim Supervisor').exists():
                    response = redirect('insurer_supervisor_dashboard')
                elif user.groups.filter(name='Insurer Audit Officer').exists():
                    response = redirect('insurer_audit_dashboard')
                elif user.groups.filter(name='Insurer Finance').exists():
                    response = redirect('insurer_finance_dashboard')
                elif user.groups.filter(name='Shield Supervisor').exists():
                    response = redirect('waadaa_supervisor')
                
            else:
                response = redirect('dashboard')  # fallback
            
         
            # Store token in a cookie or session (secure=True recommended in production)
            response.set_cookie('auth_token', token, httponly=True, secure=False)
            return response
        else:
            messages.error(request, 'Email or password is incorrect')
            return render(
                request,
                # {'error_message': 'Invalid username or password.'},
                template_name=self.template_name,
            )
        # else:
        #     return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    

class RegisterView(generics.GenericAPIView):
    renderer_classes=[TemplateHTMLRenderer]
    template_name = 'accounts/register.html'
    serializer_class = CustomUserRegisterSerializer
    permission_classes=[AllowAny]

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)
        

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": CustomUserSerializer(user).data,
                "token": AuthToken.objects.create(user)[1]
            })

def email_config_view(request):
    template_name = 'accounts/email_config.html'
    return render(request, template_name=template_name)


def getEmailConfigList(request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        queryset=EmailConfiguration.objects.all().order_by('-id')      
        # Grabing data with Search value        
        if search_value:
            queryset =  queryset.filter(
                Q(host_user__icontains=search_value) |
                Q(host_user__icontains=search_value) 
            )
        # counting All records           
        total_records = EmailConfiguration.objects.count()
        #Count Filetred Data
        filtered_records = queryset.count()
        # Range query data
        emails=queryset[start:start+length]
        #Paginate Query data
        # Serilization by Data        
        serializer = EmailConfigurationListSerializer(emails, many=True)
        # Response Data
        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': serializer.data
        })


def getUserList(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    queryset=CustomUser.objects.all().order_by('-id')      
    # Grabing data with Search value        
    if search_value:
        queryset =  queryset.filter(
            Q(email__icontains=search_value) |
            Q(username__icontains=search_value) |
            Q(phone_number__icontains=search_value) 
        )
    # counting All records           
    total_records = CustomUser.objects.count()
    #Count Filetred Data
    filtered_records = queryset.count()
    # Range query data
    users=queryset[start:start+length]
    #Paginate Query data
    # Serilization by Data        
    serializer = CustomUserListSerializer(users, many=True)
    
    # Response Data
    return JsonResponse({
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': filtered_records,
        'data': serializer.data
    })


def getEditLogs(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    queryset=EditLog.objects.all().order_by('-id')      
    # Grabing data with Search value        
    if search_value:
        queryset =  queryset.filter(
            Q(field_name__icontains=search_value) |
            Q(old_value__icontains=search_value) |
            Q(user__username__icontains=search_value) |
            Q(model_name__icontains=search_value) 
        )
    # counting All records           
    total_records = EditLog.objects.count()
    #Count Filetred Data
    filtered_records = queryset.count()
    # Range query data
    users=queryset[start:start+length]
    #Paginate Query data
    # Serilization by Data        
    serializer = EditLogSerializer(users, many=True)
    
    # Response Data
    return JsonResponse({
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': filtered_records,
        'data': serializer.data
    })


def getEmailTemplateList(request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        queryset=EmailTemplate.objects.all().order_by('-id')      
        # Grabing data with Search value        
        if search_value:
            queryset =  queryset.filter(
                Q(user__email__icontains=search_value) |
                Q(group__name__icontains=search_value) 
            )
        # counting All records           
        total_records = EmailTemplate.objects.count()
        #Count Filetred Data
        filtered_records = queryset.count()
        # Range query data
        emails=queryset[start:start+length]
        #Paginate Query data
        # Serilization by Data        
        serializer = EmailTemplateListSerializer(emails, many=True)
        # Response Data
        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': serializer.data
        })


@login_required
@api_view(["POST"])
def change_password(request):
    if request.method == 'POST':
        user = request.user
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('password')
        new_password2 = request.POST.get('confirm_password')
        # Check old password
        if not user.check_password(old_password):
            return JsonResponse({'status': 'error', 'message': 'Old password is incorrect.'})
        # Check new password match
        if new_password1 != new_password2:
            return JsonResponse({'status': 'error', 'message': 'New passwords do not match.'})
        # Set new password
        user.set_password(new_password1)
        user.system_generate='N'
        user.save()
        update_session_auth_hash(request, user)  # keep user logged in
        request.session['system_generate'] = 'N'
        request.session.modified = True
        return JsonResponse({'status': 'success', 'message': 'Password changed successfully!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

    
def logoutUser(request):
    logout(request)
    return redirect('login')



@csrf_exempt
def get_templates(request):
    """Return both group-wise and user-wise templates separately"""
    group_templates = EmailTemplate.objects.filter(template_type='group', is_active=True).values(
        'id', 'group__name', 'subject', 'message'
    )
    user_templates = EmailTemplate.objects.filter(template_type='user', is_active=True).values(
        'id', 'user__username', 'subject', 'message'
    )

    return JsonResponse({
        "group_templates": list(group_templates),
        "user_templates": list(user_templates)
    })


def get_edit_log_view(request):
    template_name = 'accounts/edit_template_logs.html'
    return render(request, template_name=template_name)

@csrf_exempt
def save_template(request):
    """Save or update an email template"""
    if request.method == "POST":
        data = request.POST
        template_type = data.get("template_type")
        subject = data.get("subject")
        message = data.get("message")
        status = data.get("file_status")
        if template_type == "group":
            group_id = data.get("group_id")
            group = Group.objects.get(id=group_id)
            EmailTemplate.objects.update_or_create(
                group=group,
                template_type="group",
                status=status,
                defaults={"subject": subject, "message": message, "is_active": True if data.get("status") == "on" else False,"status":status}
            )

        # elif template_type == "user":
        #     user_id = data.get("user_id")
        #     user = CustomUser.objects.get(id=user_id)
        #     EmailTemplate.objects.update_or_create(
        #         user=user,
        #         template_type="user",
        #         defaults={"subject": subject, "message": message, "is_active": True}
        #     )

        return JsonResponse({"success": True, "message": "Template saved successfully!"})


@csrf_exempt
def get_email_config(request):
    """Return the active email configuration"""
    config = EmailConfiguration.objects.filter(is_active=True).first()
    if not config:
        return JsonResponse({"error": "No active configuration found"}, status=404)
    return JsonResponse({
        "id": config.id,
        "smtp_host": config.host,
        "port": config.port,
        "tls": config.use_tls,
        "ssl": config.use_ssl,
        "sender_email": config.host_user,
        "is_active":config.is_active,
        "host_password":config.host_password
    })


def email_template_view(request):
    groups=Group.objects.all()
    template_name = 'accounts/email_template.html'
    context = {
            "groups": groups,
    }
    return render(request, template_name=template_name,context=context)

def user_create_view(request):
    groups=Group.objects.all()
    template_name = 'accounts/user_template.html'
    context = {
            "groups": groups,
    }
    return render(request, template_name=template_name,context=context)


class UserCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"success":True,"message": "User created successfully", "user_id": user.id},
                status=status.HTTP_201_CREATED
            )
        print({"success":False,"data":serializer.errors})
        return Response({"success":False,"data":serializer.errors})

@csrf_exempt
def save_email_config(request):
    """Save or update email configuration"""
    if request.method == "POST":
        data = request.POST
        config, _ = EmailConfiguration.objects.update_or_create(
            defaults={
                "host": data.get("smtp_host"),
                "port": data.get("port"),
                "use_tls":True if data.get("tls") == "on" else False,
                "use_ssl":True if data.get("ssl") == "on" else False,
                "host_user": data.get("sender_email"),
                "host_password": data.get("app_password"),
                "is_active":True if data.get("status") == "on" else False,
            }
        )
        return JsonResponse({"success": "true", "message": "Email configuration saved!"})


class EmailTemplateView(APIView):
    queryset = EmailTemplate.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmailTemplateListSerializer
    def get(self, request,pk):
        try:
            template = EmailTemplate.objects.get(pk=pk) #Serialize single item
            serializer = EmailTemplateListSerializer(template)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except EmailTemplate.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        data = request.POST.copy()  # make QueryDict mutable
        try:
            template = EmailTemplate.objects.get(pk=pk)
        except EmailTemplate.DoesNotExist:
            return Response({"error": "Template not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(template, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True,"data":serializer.data}, status=status.HTTP_200_OK)
        return Response({"success":True,"data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    queryset = CustomUser.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomUserListSerializer
    def get(self, request,pk):
        try:
            user = CustomUser.objects.get(pk=pk) #Serialize single item
            serializer = CustomUserListSerializer(user)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        data = request.data.copy()  # make mutable
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"success": False, "error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # If password is not provided, remove it so serializer won't overwrite it
        if  data.get('update_password') !='':
            data['password'] =data.get('update_password', None)
            data['confirm_password'] =data.get('update_confirm_password', None)


        is_active_value = data.get('is_active')  
        if  is_active_value == 'on':
            data['is_active']=True
            data['is_staff']=True
        else:
            data['is_active']= False
            data['is_staff']= False      
        serializer = self.serializer_class(user, data=data, partial=True)  # partial=True allows partial update
        if serializer.is_valid():
            # Handle password separately
            password = serializer.validated_data.pop('password', None)
            serializer.save()
            if data.get('update_password') !='':
                user.set_password(data.get('update_password',None))
                user.save()

            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, "data": serializer.errors})
    

def user_group_view(request):
    template_name = 'accounts/groups.html'
    return render(request, template_name=template_name)



class GroupView(APIView):
    queryset = CustomUser.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = GroupSerializer
    def get(self, request,pk):
        try:
            user = Group.objects.get(pk=pk) #Serialize single item
            serializer = GroupSerializer(user)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Group.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        data = request.data.copy()  # make mutable
        try:
            user = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response({"success": False, "error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        data['name'] = data.get('groupname')  
        is_active_value = data.get('is_active')  
        if  is_active_value == 'on':
            data['active']=True
        else:
            data['active']= False
        serializer = self.serializer_class(user, data=data, partial=True)  # partial=True allows partial update
        if serializer.is_valid():
            # Handle password separately
            serializer.save()

            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, "data": serializer.errors})

    def delete(self, request, pk):
        group = Group.objects.filter(id=pk).first()
        if not group:
            return Response({"detail": "Group not found"}, status=404)

        group.delete()
        return Response({"detail": "Group deleted successfully"}, status=204)

def getGroupList(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    queryset=Group.objects.all().order_by('-id')      
    # Grabing data with Search value        
    if search_value:
        queryset =  queryset.filter(
            Q(name__icontains=search_value) 
        
        )
    # counting All records           
    total_records = Group.objects.count()
    #Count Filetred Data
    filtered_records = queryset.count()
    # Range query data
    users=queryset[start:start+length]
    #Paginate Query data
    # Serilization by Data        
    serializer = GroupSerializer(users, many=True)
    
    # Response Data
    return JsonResponse({
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': filtered_records,
        'data': serializer.data
    })
    
    

class GroupCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"success":True,"message": "Group created successfully"},
                status=status.HTTP_201_CREATED
            )
        print({"success":False,"data":serializer.errors})
        return Response({"success":False,"data":serializer.errors})



@group_required_multiple('Super Admin')
def database_backup(request):
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"backup_{now}.json"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    with open(filepath, 'w') as file:
        call_command('dumpdata', stdout=file)

    with open(filepath, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
    

@api_view(['POST'])
def login_api(request):
    identifier = request.data.get('username')  # can be username or email
    password = request.data.get('password')
    # find user by username or email
    try:
        user_obj = CustomUser.objects.filter(
            Q(phone_number=identifier) | Q(email=identifier)
        ).get()
    except CustomUser.DoesNotExist:
        return Response({ "success":False,"message": "Invalid mobile/email or password"}, status=400)
    if user_obj.groups.filter(name='B2B Employee').exists():
    # authenticate using username
        user = authenticate(email=user_obj.email, password=password)
        if user is None:
            user = authenticate(phone_number=IndentationError, password=password)
        if user is None:
            return Response({ "success":False,"message": "Invalid mobile/email or password"}, status=400)

        token, created = Token.objects.get_or_create(user=user)
        user_data = CustomUserListSerializer(user).data

        return Response({
            "success":True,
            "message": "Login successful",
            "token": token.key,
            "user": user_data
        })
    return Response({ "success":False,"message": "User is not authonticated"}, status=400)

   