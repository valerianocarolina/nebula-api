from django.contrib import admin

from .models import FriendRequest, Follow

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
  list_display = (
    'id',
    'sender',
    'receiver',
    'status',
    'created_at',
  )

  list_filter = (
    'status',
  )

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
  list_display = (
    'id',
    'follower',
    'following',
    'created_at',
  )