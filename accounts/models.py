from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
import re


class AccountUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # Set role as ADMIN for superuser
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrator'
    PARISH_PRIEST = 'PARISH_PRIEST', 'Parish Priest'
    BODY_MEMBER = 'BODY_MEMBER', 'Body Member'
    FAMILY_HEAD = 'FAMILY_HEAD', 'Family Head'


class BodyMemberSubRole(models.TextChoices):
    PRESIDENT = 'PRESIDENT', 'President'
    VICE_PRESIDENT = 'VICE_PRESIDENT', 'Vice President'
    TREASURER = 'TREASURER', 'Treasurer'


def validate_indian_mobile(value):
    """
    Validates Indian 10-digit mobile numbers.
    Must start with 6, 7, 8, or 9 and be exactly 10 digits long.
    """
    pattern = re.compile(r'^[6-9]\d{9}$')
    if not pattern.match(value):
        raise ValidationError('Enter a valid 10-digit Indian mobile number (starting with 6–9).')


class AccountUser(AbstractUser):
    username = None # Remove username field
    email = None  # Remove email field
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.FAMILY_HEAD
    )
    sub_role = models.CharField(
        max_length=30,
        choices=BodyMemberSubRole.choices,
        blank=True,
        null=True,
        help_text="Optional sub-role if role is BODY_MEMBER"
    )
    phone_number = models.CharField(max_length=10,
                                    unique=True,
                                    validators=[validate_indian_mobile],
                                    help_text="10-digit Indian mobile number starting with 6-9")
    address = models.TextField(blank=True)
    
    # override groups and permissions to avoid clashes with AbstractUser
    groups = models.ManyToManyField(
        Group,
        related_name='accountuser_groups_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='accountuser_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = AccountUserManager()
    
    def __str__(self):
        return f"{self.phone_number} - {self.get_role_display()}"
    
    def clean(self):
        super().clean()
        if self.sub_role and self.role != UserRole.BODY_MEMBER:
            raise ValidationError("Sub-role can only be set for Body Members")
