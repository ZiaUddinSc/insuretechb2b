import os
import uuid
from django.db import models
from django.contrib import messages
from django.contrib.auth.models import AbstractUser,AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import Group
from .managers import CustomUserManager
# Create your models here.

"""User Profile Photo"""
def user_photo_file_path(instance, filename):
    """Generate file path for new image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('userprofilephoto/', filename)



"""Phone No Validation"""
phone_validator = RegexValidator(
    regex=r'^\+?1?\d{10,11}$',
    message="Phone number must be entered in the format: '+880'. Up to 11 digits allowed."
)


"""Gender Choices"""
GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]


"""Blood Groups"""
BLOOD_GROUPS = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    )


"""Marital Status"""    
MARITAL_STATUS = (
    ('S', 'Single'),
    ('M', 'Married'),
    ('D', 'Divorced'),
    ('W', 'Widowed')
)

"""Common Use for all models"""
class AuditBaseModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    # updated_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="%(class)s_updated",
    # )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 

    class Meta:
        abstract = True

"""Permission"""
class Permissions(AuditBaseModel):
    codename = models.CharField(max_length=100, unique=True,null=True, blank=True)
    name = models.CharField(max_length=150,null=True, blank=True)


    def __str__(self):
        return f"{self.name}"
    

    class Meta:
        db_table = 'permissions'
        ordering = ['-id']  # Orders by id in descending order


"""Role"""
class Role(AuditBaseModel):
    name = models.CharField(max_length=100, unique=True,null=True, blank=True)
    permissions = models.ManyToManyField(Permissions, blank=True)


    def __str__(self):
        return f"{self.name}"


    class Meta:
        db_table = 'role'
        ordering = ['-id']  # Orders by id in descending order


class CustomUser(AbstractBaseUser, PermissionsMixin,AuditBaseModel):
    """Gender Choices"""
    SYSTEM_GENARATE_CHOICES = [
        ('Y', 'YES'),
        ('N', 'NO'),
    ]

    """Custom User Information"""
    username = models.CharField(max_length=17, blank=True,null=True)
    email = models.EmailField(unique=True, blank=True,null=True)
    first_name = models.CharField(max_length=50, blank=True,null=True)
    last_name = models.CharField(max_length=50, blank=True,null=True)
    phone_number = models.CharField(unique=True, max_length=17,blank=True,null=True)
    user_id = models.CharField(max_length=50, unique=True, blank=True,null=True)
    is_status = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    system_generate =  models.CharField(
        max_length=5,
        choices=SYSTEM_GENARATE_CHOICES,
        default='N',
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

    def __str__(self):
        if self.username:
            return f"{self.username}" if self.username else None
        elif self.email:
            return f"{self.email}" if self.email else None
        else:
            return None
        
    
    def save(self, *args, **kwargs):
        """UID->>> User Identification"""
        if not self.phone_number:
            # self.user_id = f'SN{str(uuid.uuid4().int)[:6]}'.upper()
            self.user_id = f'UID{str(uuid.uuid4().hex[:6]).upper()}' 
        if not self.username:
            # self.user_id = f'SN{str(uuid.uuid4().int)[:6]}'.upper()
            self.user_id = f'UID{str(uuid.uuid4().hex[:6]).upper()}' 
        if not self.email:
            # self.user_id = f'SN{str(uuid.uuid4().int)[:6]}'.upper()
            self.user_id = f'UID{str(uuid.uuid4().hex[:6]).upper()}' 
        super().save(*args, **kwargs)
    

   
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True


    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    

    class Meta:
        db_table = 'custom_user'
        ordering = ['-id']  # Orders by id in descending order




class EmailConfiguration(models.Model):
    name = models.CharField(max_length=100, default='Default Config')
    host = models.CharField(max_length=200, help_text="SMTP host, e.g. smtp.gmail.com")
    port = models.IntegerField(default=587)
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)
    host_user = models.EmailField(help_text="Sender email address")
    host_password = models.CharField(max_length=255, help_text="Email app password or SMTP key")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.host_user})"


class EmailTemplate(models.Model):
    TEMPLATE_TYPE_CHOICES = [
        ('group', 'Group Template'),
        ('user', 'User Template'),
    ]
    
    FILE_TYPE_CHOICES = [
    (0, 'DECLINED'),
    (1, 'APPROVED'),
    (2, 'SUBMITTED'),
    (3, 'SETTELED'),
    (4, 'PENDING'),
    (5, 'PROCESSING'),
    (6, 'RETURN'),
    (7, 'DOCUMENT-WANTED'),
    
]

    template_type = models.CharField(max_length=10, choices=TEMPLATE_TYPE_CHOICES)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    # user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.PositiveBigIntegerField(default=1, choices=FILE_TYPE_CHOICES)   

    class Meta:
        verbose_name = "Email Template"
        verbose_name_plural = "Email Templates"

    # def __str__(self):
    #     if self.template_type == 'group' and self.group:
    #         return f"{self.group.name} (Group Template)"
    #     elif self.template_type == 'user' and self.user:
    #         return f"{self.user.username} (User Template)"
    #     return f"{self.template_type.capitalize()} Template"
    


class EditLog(models.Model):
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField()
    field_name = models.CharField(max_length=100)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_name} ({self.object_id}) - {self.field_name}"