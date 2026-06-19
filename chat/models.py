from django.db import models
from django.conf import settings

class Conversation(models.Model):
  participants = models.ManyToManyField(
    settings.AUTH_USER_MODEL,
    related_name='conversations'
  )

  created_at = models.DateTimeField(
    auto_now_add=True
  )

  def __str__(self):
    return f'Conversation {self.id}'

class Message(models.Model):
  conversation = models.ForeignKey(
    Conversation,
    on_delete=models.CASCADE,
    related_name='messages'
  )

  sender = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='sent_messages'
  )

  text = models.TextField()

  created_at = models.DateTimeField(
    auto_now_add=True,
    db_index=True
  )

  is_read = models.BooleanField(
    default=False
  )

  class Meta:
    ordering = ['created_at']

    indexes = [
      models.Index(fields=['created_at']),
    ]

  def __str__(self):
    return (
      f'{self.sender.username} '
      f'- Conversation {self.conversation.id}'
    )