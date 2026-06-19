from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import F, Q

class FriendRequest(models.Model):
  class Status(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    ACCEPTED = 'ACCEPTED', 'Accepted'
    REJECTED = 'REJECTED', 'Rejected'

  sender = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='sent_friend_requests'
  )

  receiver = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='received_friend_requests'
  )

  status = models.CharField(
    max_length=10,
    choices=Status.choices,
    default=Status.PENDING
  )

  created_at = models.DateTimeField(
    auto_now_add=True
  )

  class Meta:
    unique_together = ['sender', 'receiver']

    constraints = [
      models.CheckConstraint(
        condition=~Q(sender=F('receiver')),
        name='friend_request_cannot_target_self',
      )
    ]

  def clean(self):
    if self.sender == self.receiver:
      raise ValidationError('Um usuário não pode enviar amizade para si mesmo.')

  def __str__(self):
    return (
      f'{self.sender.username} -> '
      f'{self.receiver.username} '
      f'({self.status})'
    )

class Follow(models.Model):
  follower = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='following_relationships'
  )

  following = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='follower_relationships'
  )

  created_at = models.DateTimeField(
    auto_now_add=True
  )

  class Meta:
    unique_together = ['follower', 'following']

    constraints = [
      models.CheckConstraint(
        condition=~Q(follower=F('following')),
        name='user_cannot_follow_self',
      )
    ]

  def clean(self):
    if self.follower == self.following:
      raise ValidationError('Um usuário não pode seguir a si mesmo.')

  def __str__(self):
    return (
      f'{self.follower.username} '
      f'follows '
      f'{self.following.username}'
    )