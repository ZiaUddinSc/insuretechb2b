from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group



"""AbstractBaseUser User can only use one like username email or phone no"""
class CustomUserManager(BaseUserManager):
    def _create_user(self,username=None, email=None, password=None,  **extra_fields):
        # Ensure at least one identifier is provided
        if not username and not email :
            raise ValidationError("You must provide at least one of the following: username, email, or phone number.")
        
        # Normalize email if provided
        if email:
            email = self.normalize_email(email)

        # Ensure only one identifier is provided
        identifiers = [bool(username), bool(email)]
        if identifiers.count(True) < 1 or identifiers.count(True)>2:
            raise ValidationError("You can only use one or two identifier: username, email, or phone number.")

        # Create the user
        user = self.model(username='Super Admin', email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        # 2. Add to group (optional)
        group, created = Group.objects.get_or_create(name='Super Admin')
        user.groups.add(group)
        return user
    

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        print("USer not foubd")
        return self._create_user(username,email, password, **extra_fields)
    

    def create_superuser(self, username=None, email=None,  password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username,email, password, **extra_fields)
    
    

