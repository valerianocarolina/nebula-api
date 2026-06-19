from django.contrib import admin

from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display = (
    'id',
    'author',
    'post',
    'created_at',
  )

  search_fields = (
    'text',
    'author__username',
  )