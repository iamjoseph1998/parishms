from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AccountUser, UserRole

@admin.register(AccountUser)
class AccountUserAdmin(UserAdmin):
    model = AccountUser
    list_display = ('phone_number', 'role', 'is_body_member', 'family', 'is_staff')
    list_filter = ('role', 'is_body_member', 'is_staff', 'family')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Info', {'fields': ('address', 'role', 'family')}),
        ('Body Member Info', {'fields': ('is_body_member', 'body_member_position')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'address', 'role', 'family', 'is_body_member', 'body_member_position', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('phone_number', 'family__name')
    ordering = ('phone_number',)

