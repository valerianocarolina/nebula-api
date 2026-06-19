from django.contrib import admin

from .models import Post, PostMedia, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']

class PostMediaInLine(admin.TabularInline):
  model = PostMedia
  extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = (
    'id',
    'author',
    'created_at',
  )

  search_fields = (
    'text',
    'author__username',
  )

  list_filter = (
    'created_at',
  )

  inlines = [PostMediaInLine]

@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
  list_display = (
    'id',
    'post',
    'media_type',
  )

  search_fields = (
    'post__text',
    'post__author__username',
  )

  list_filter = (
    'media_type',
  )