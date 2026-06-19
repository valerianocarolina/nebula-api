from django.db import models
from django.conf import settings

from posts.models import Post

class Reaction(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='reactions'
  )

  post = models.ForeignKey(
    Post,
    on_delete=models.CASCADE,
    related_name='reactions'
  )

  created_at = models.DateTimeField(
    auto_now_add=True
  )

  class Meta:
    unique_together = ['user', 'post']

  def __str__(self):
    return f'{self.user.username} liked post {self.post.id}'