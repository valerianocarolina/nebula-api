from django.db import models
from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Report(models.Model):
  class Status(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    RESOLVED = 'RESOLVED', 'Resolved'
    DISMISSED = 'DISMISSED', 'Dismissed'

  reporter = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='reports'
  )

  reason = models.TextField()

  status = models.CharField(
    max_length=10,
    choices=Status.choices,
    default=Status.PENDING
  )

  created_at = models.DateTimeField(
    auto_now_add=True
  )

  content_type = models.ForeignKey(
    ContentType,
    on_delete=models.CASCADE
  )

  object_id = models.PositiveIntegerField()

  reported_object = GenericForeignKey(
    'content_type',
    'object_id'
  )

  class Meta:
    ordering = ['-created_at']

    indexes = [
      models.Index(
        fields=['content_type', 'object_id']
      )
    ]

  def __str__(self):
    return (
      f'Report #{self.id} '
      f'({self.status})'
    )