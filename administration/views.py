from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from posts.models import Post
from reports.models import Report

from reports.permissions import IsAdmin

User = get_user_model()

class AdminCreateUserView(
  APIView
):
  permission_classes = [
    IsAdmin
  ]

  def post(
    self,
    request
  ):
    username = request.data.get(
      'username'
    )

    email = request.data.get(
      'email'
    )

    password = request.data.get(
      'password'
    )
    
    if User.objects.filter(
      username=username
    ).exists():
      return Response(
        {
          'detail':
          'Username já existe.'
        },
        status=status.HTTP_400_BAD_REQUEST
      )
    
    user = User.objects.create(
      username=username,
      email=email,
      role='ADMIN',
    )

    user.set_password(
      password
    )

    user.save()

    return Response(
      {
        'id': user.id,
        'username': user.username,
        'role': user.role,
      },
      status=status.HTTP_201_CREATED
    )
  
class AdminDeleteUserView(
  APIView
):
  permission_classes = [
    IsAdmin
  ]

  def delete(
    self,
    request,
    pk
  ):
    user = get_object_or_404(
      User,
      pk=pk
    )

    if user.role == 'ADMIN':
      return Response(
        {
          'detail':
          'Não é permitido remover outro administrador.'
        },
        status=status.HTTP_400_BAD_REQUEST
      )
    
    user.is_active = False

    user.save(
      update_fields=[
        'is_active'
      ]
    )

    return Response(
      {
        'detail':
        'Usuário desativado.'
      }
    )
  
class AdminDeletePostView(
  APIView
):
  permission_classes = [
    IsAdmin
  ]

  def delete(
    self,
    request,
    pk
  ):
    post = get_object_or_404(
      Post,
      pk=pk
    )

    post.delete()

    return Response(
      {
        'detail':
        'Post removido.'
      }
    )
  
class AdminDashboardView(
  APIView
):
  permission_classes = [
    IsAdmin
  ]

  def get(
    self,
    request
  ):
    return Response(
      {
        'users_count':
        User.objects.count(),

        'active_users_count':
        User.objects.filter(
          is_active=True
        ).count(),

        'posts_count':
        Post.objects.count(),

        'pending_reports_count':
        Report.objects.filter(
          status=Report.Status.PENDING
        ).count(),

        'resolved_reports_count':
        Report.objects.filter(
          status=Report.Status.RESOLVED
        ).count(),
      }
    )