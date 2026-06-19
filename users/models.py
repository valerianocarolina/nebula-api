from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
  class Role(models.TextChoices):
    COMMON = 'COMMON', 'Common'
    ADMIN = 'ADMIN', 'Admin'

  bio = models.TextField(
    blank=True,
    null=True,
  )

  avatar = models.ImageField(
    upload_to='avatars/',
    blank=True,
    null=True,
  )

  is_private = models.BooleanField(
    default=False
  )

  role = models.CharField(
    max_length=10,
    choices=Role.choices,
    default=Role.COMMON
  )

  def __str__(self):
    return self.username
