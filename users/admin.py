from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
  fieldsets = UserAdmin.fieldsets + (
    (
      'Profile',
      {
        'fields': (
          'bio',
          'avatar',
          'is_private',
          'role',
        )
      },
    ),
  )

  list_display = (
    'id',
    'username',
    'email',
    'role',
    'is_private',
    'is_staff',
  )

  list_filter = (
    'role',
    'is_private',
    'is_staff',
  )