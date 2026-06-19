from django.contrib import admin

from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
  list_display = (
    'id',
    'reporter',
    'status',
    'content_type',
    'object_id',
    'created_at',
  )

  list_filter = (
    'status',
    'content_type',
  )

  search_fields = (
    'reason',
  )