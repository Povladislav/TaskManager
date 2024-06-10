from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from authentication.models import User


class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'first_name', 'second_name', 'patronymic', 'phone_number', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'second_name', 'patronymic', 'phone_number', 'role', 'password1',
                'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'second_name', 'patronymic', 'phone_number', 'role', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'second_name', 'patronymic', 'phone_number')
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
