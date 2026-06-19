from django.contrib import admin

from .models import Reaction

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
  list_display = (
    'id',
    'user',
    'post',
    'created_at',
  )

  search_fields = (
    'user__username',
  )