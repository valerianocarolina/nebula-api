from django.db import models
from django.conf import settings

from posts.models import Post

class Comment(models.Model):
  post = models.ForeignKey(
    Post,
    on_delete=models.CASCADE,
    related_name='comments'
  )

  author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='comments'
  )

  parent = models.ForeignKey(
    'self',
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name='replies',
  )

  text = models.TextField()

  created_at = models.DateTimeField(
    auto_now_add=True
  )

  class Meta:
    ordering = ['created_at']

  def __str__(self):
    return (
      f'{self.author.username} '
      f'- Post {self.post.id} '
    )