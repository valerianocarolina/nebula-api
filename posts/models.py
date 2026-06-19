from django.db import models
from django.conf import settings

class Tag(models.Model):
  name = models.CharField(
    max_length=100,
    unique=True
  )

  def __str__(self):
    return self.name

class Post(models.Model):
  author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='posts'
  )

  text = models.TextField()

  tags = models.ManyToManyField(
    Tag,
    blank=True,
    related_name='posts'
  )

  created_at = models.DateTimeField(
    auto_now_add=True
  )

  updated_at = models.DateTimeField(
    auto_now=True
  )

  class Meta:
    ordering = ['-created_at']

  def __str__(self):
    return f'{self.author.username} - {self.created_at}'

class PostMedia(models.Model):
  class MediaType(models.TextChoices):
    IMAGE = 'IMAGE', 'Image'
    VIDEO = 'VIDEO', 'Video'

  post = models.ForeignKey(
    Post,
    on_delete=models.CASCADE,
    related_name='medias'
  )

  file = models.FileField(
    upload_to='posts/media/'
  )

  media_type = models.CharField(
    max_length=10,
    choices=MediaType.choices
  )

  def __str__(self):
    return f'{self.media_type} - Post {self.post.id}'