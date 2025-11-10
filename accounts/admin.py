from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AccountUser

@admin.register(AccountUser)
class AccountUserAdmin(UserAdmin):
    model = AccountUser
    list_display = ('phone_number', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Info', {'fields': ('address', 'role', 'sub_role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'role', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
