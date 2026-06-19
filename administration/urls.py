from django.urls import path

from administration.views import (
  AdminCreateUserView,
  AdminDeleteUserView,
  AdminDeletePostView,
  AdminDashboardView,
)

urlpatterns = [
  path(
    'admin/users/',
    AdminCreateUserView.as_view(),
    name='admin-create-user',
  ),

  path(
    'admin/users/<int:pk>/',
    AdminDeleteUserView.as_view(),
    name='admin-delete-user',
  ),

  path(
    'admin/posts/<int:pk>/',
    AdminDeletePostView.as_view(),
    name='admin-delete-post',
  ),

  path(
    'admin/dashboard/',
    AdminDashboardView.as_view(),
    name='admin-dashboard',
  )
]