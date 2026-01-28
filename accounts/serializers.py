from rest_framework import serializers
from rest_framework import generics, status
from django.contrib.auth.models import Group
from rest_framework.response import Response
from .models import ( CustomUser, EditLog,EmailConfiguration,EmailTemplate)
from django.utils.timesince import timesince



class GroupSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(required=False)
    class Meta:
        model = Group
        fields =  ['id', 'name']


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(required=False)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        # Handle empty or None username
        if not value:
            return None
        # Check if username already exists (ignoring the current instance)
        if self.instance:
            # Exclude current instance from uniqueness check
            if CustomUser.objects.filter(username=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This username is already in use.")
        else:
            # If creating, just check if it exists
            if CustomUser.objects.filter(username=value).exists():
                raise serializers.ValidationError("This username is already in use.")
        
        return value
        

    def validate_email(self, value):
        # Handle empty or None email
        if not value:
            return None
        # Check if email already exists (ignoring the current instance)
        if self.instance:
            # Exclude current instance from uniqueness check
            if CustomUser.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This email is already in use.")
        else:
            # If creating, just check if it exists
            if CustomUser.objects.filter(email=value).exists():
                raise serializers.ValidationError("This email is already in use.")
        
        return value
    
    def validate_phone_number(self, value):
        # Handle empty or None phone_number
        if not value:
            return None
        # Check if phone_number already exists (ignoring the current instance)
        if self.instance:
            # Exclude current instance from uniqueness check
            if CustomUser.objects.filter(phone_number=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This phone_number is already in use.")
        else:
            # If creating, just check if it exists
            if CustomUser.objects.filter(phone_number=value).exists():
                raise serializers.ValidationError("This phone_number is already in use.")
        
        return value

        
    
    def validate_username(self, data):
        """Validate if the input is a valid email or phone."""
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        data = str(data).strip()
        # Check if it's an email
        try:
            validate_email(data)
            # self.validated_data['email'] = data
            self.is_email = True
            return data
        except ValidationError:
            # self.is_email = False
            pass

        # Check if it's a phone number
        # if not data.isdigit() or len(data) < 11 or len(data) > 11:
        # if not str(data).isdigit() or len(str(data)) != 11 or not validate_email(data):
        #     print('phone',data,type(data['username']),len(str(data)) == 11,str(data).isdigit())
        #     raise serializers.ValidationError("Enter a valid phone number or email.")
        # self.validated_data['phone_number'] = data
        # return data
        # Check if it's a valid phone number (only digits and exactly 11 characters)
        if data.isdigit() and len(data) == 11:
        #     raise serializers.ValidationError("Phone number should contain only digits.")
        # if len(data) != 11:
        #     raise serializers.ValidationError("Phone number must be exactly 11 digits.")

            self.is_email = False
            return data
        raise serializers.ValidationError("Enter a valid phone number or email.")


        

    def create(self, validated_data):
        email = validated_data['email']
        # password = validated_data['password']
        password = validated_data.pop('password')

        if hasattr(self, 'is_email') and email:
            user = CustomUser.objects.create_user(email=email)
        else:
            user = CustomUser.objects.create_user(email=email)
        # user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class CustomUserListSerializer(serializers.ModelSerializer):
    # roles = RoleSerializer(many=True)
    groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Group.objects.all(), required=False
    )
    group_details = GroupSerializer(source='groups', many=True, read_only=True)
    group_names = serializers.SerializerMethodField()

    def get_group_names(self, obj):
        """Return comma-separated group names"""
        return ", ".join([group.name for group in obj.groups.all()])
    
    class Meta:
        model = CustomUser
        fields = ['id','first_name','last_name', 'email', 'username','is_active','phone_number','groups','group_details','group_names']



class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Group.objects.all(), required=False
    )

    class Meta:
        model = CustomUser
        fields = [
            'email',
            "username",
            "phone_number",
            'password',
            'confirm_password',
            'groups',
            'is_staff',
            'is_active',
        ]

    def to_internal_value(self, data):
        """
        Convert 'on'/'off' or similar string values for is_active to boolean.
        """
        data = super().to_internal_value(data)
        is_active_value = self.initial_data.get('is_active')

        if isinstance(is_active_value, str):
            data['is_active']   = is_active_value.lower() == 'on' if isinstance(is_active_value, str) else False
            data['is_staff']    = False
        return data

    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        validated_data.pop('confirm_password')

        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        
        user.set_password(password)
        user.save()

        if groups:
            user.groups.set(groups)

        return user


class CustomUserSerializer(serializers.ModelSerializer):
    # roles = RoleSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username']

class FileUploadSerializer(serializers.Serializer):
    user_files = serializers.FileField()
    default_password = serializers.CharField(required=False)


class EmailConfigurationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfiguration
        fields = '__all__' 


class EditLogSerializer(serializers.ModelSerializer):
    user_display = serializers.SerializerMethodField()
    time_ago = serializers.SerializerMethodField()
    change_summary = serializers.SerializerMethodField()

    class Meta:
        model = EditLog
        fields = [
            'id',
            'model_name',
            'object_id',
            'field_name',
            'old_value',
            'new_value',
            'user_display',
            'time_ago',
            'changed_at',
            'change_summary',
        ]

    def get_user_display(self, obj):
        if obj.user:
            return obj.user.username or obj.user.email
        return "System"

    def get_time_ago(self, obj):
        return f"{timesince(obj.changed_at)} ago"

    def get_change_summary(self, obj):
        old = obj.old_value or "—"
        new = obj.new_value or "—"
        return f"{obj.field_name} changed from '{old}' to '{new}'"
    class Meta:
        model = EditLog
        fields = '__all__' 


class EmailTemplateListSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True,allow_null=True)
    template_type_display = serializers.CharField(source='get_template_type_display', read_only=True, required=False)
    status_display = serializers.CharField(source='get_status_display', read_only=True, required=False)
    class Meta:
        model = EmailTemplate
        fields = '__all__' 