from django.contrib import admin
from .models import CustomUser,EmailConfiguration,EmailTemplate,EditLog
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_staff','is_active')
    list_filter = ('is_staff', 'is_active')

    ordering = ('email',)
    search_fields = ('email', 'username')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions','system_generate')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'groups','is_staff', 'is_active'),
        }),
    )

admin.site.register(Permission)
admin.site.register(EmailConfiguration)
admin.site.register(EmailTemplate)
admin.site.register(EditLog)