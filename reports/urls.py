from django.urls import path

from reports.views import (
  ReportCreateView,
  AdminReportListView,
  AdminReportUpdateView,
)

urlpatterns = [
  path(
    'reports/',
    ReportCreateView.as_view(),
    name='report-create',
  ),

  path(
    'admin/reports/',
    AdminReportListView.as_view(),
    name='admin-report-list',
  ),

  path(
    'admin/reports/<int:pk>/',
    AdminReportUpdateView.as_view(),
    name='admin-report-update',
  ),
]