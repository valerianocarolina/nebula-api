from rest_framework import status, generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import (
  TokenObtainPairView,
)

from users.throttles import (
  LoginRateThrottle,
)

from users.serializers import RegisterSerializer

from friendships.models import (
  Follow,
)

from users.serializers import (
  LogoutSerializer,
  UserPublicSerializer,
)

from users.permissions import (
  IsProfilePublicOrFriend,
)

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .serializers import (
  UserPublicSerializer,
  UserDetailSerializer,
  ChangePasswordSerializer,
)

from config.pagination import (
  UserPagination,
)

User = get_user_model()

class RegisterView(APIView):
  permission_classes = [
    permissions.AllowAny
  ]

  def post(self, request):
    serializer = RegisterSerializer(
      data=request.data
    )

    serializer.is_valid(
      raise_exception=True
    )

    user = serializer.save()

    refresh = RefreshToken.for_user(
      user
    )

    return Response(
      {
        'user_id': user.id,
        'username': user.username,
        'access': str(
          refresh.access_token
        ),
        'refresh': str(refresh),
      },
      status=status.HTTP_201_CREATED,
    )

class LogoutView(APIView):
  permission_classes = [
    permissions.IsAuthenticated
  ]

  def post(self, request):
    serializer = LogoutSerializer(
      data=request.data
    )

    serializer.is_valid(
      raise_exception=True
    )

    try:
      token = RefreshToken(
        serializer.validated_data[
          'refresh'
        ]
      )

      token.blacklist()

      return Response(
        {
          'detail':
          'Logout realizado com sucesso.'
        }
      )

    except Exception:
      return Response(
        {
          'detail':
          'Refresh token inválido.'
        },
        status=status.HTTP_400_BAD_REQUEST,
      )

class MeView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    serializer = UserDetailSerializer(request.user)
    return Response(serializer.data)

  def patch(self, request):
    serializer = UserDetailSerializer(
      request.user,
      data=request.data,
      partial=True
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)

class ChangePasswordView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
    serializer = ChangePasswordSerializer(
      data=request.data
    )

    serializer.is_valid(raise_exception=True)

    if not request.user.check_password(
      serializer.validated_data["old_password"]
    ):
      return Response(
        {"detail": "Senha atual incorreta."},
        status=status.HTTP_400_BAD_REQUEST
      )

    request.user.set_password(
      serializer.validated_data["new_password"]
    )

    request.user.save()

    return Response(
      {"detail": "Senha alterada com sucesso."}
    )

class UserProfileView(APIView):
  permission_classes = [AllowAny]

  def get(self, request, username):
    user = get_object_or_404(
      User,
      username=username
    )

    permission = (
      IsProfilePublicOrFriend()
    )

    if not permission.has_object_permission(
      request,
      self,
      user
    ):
      return Response(
        {
          'id': user.id,
          'username': user.username,
          'is_private': True,
        }
      )

    serializer = UserPublicSerializer(user)

    return Response(serializer.data)

class UserSearchView(APIView):
  permission_classes = [AllowAny]

  def get(self, request):
    query = request.query_params.get("q")

    if not query:
      return Response([])

    users = User.objects.filter(
      Q(username__icontains=query)
      |
      Q(first_name__icontains=query)
      |
      Q(last_name__icontains=query)
    )

    paginator = UserPagination()

    page = paginator.paginate_queryset(
      users,
      request,
    )

    serializer = UserPublicSerializer(
      page,
      many=True
    )

    return paginator.get_paginated_response(serializer.data)
  
class FollowToggleView(
  APIView
):
  permission_classes = [
    IsAuthenticated
  ]

  def post(
    self,
    request,
    username
  ):
    user = (
      get_object_or_404(
        User,
        username=username
      )
    )

    if user == request.user:
      return Response(
        {
          'detail':
          'Você não pode seguir a si mesmo.'
        },
        status=status.HTTP_400_BAD_REQUEST
      )

    follow, created = Follow.objects.get_or_create(
      follower=request.user,
      following=user,
    )

    if not created:
      follow.delete()

      return Response(
        {
          'detail':
          'Unfollow realizado.'
        }
      )

    return Response(
      {
        'detail':
        'Agora você segue este usuário.'
      }
    )

    if follow:
      follow.delete()

      return Response(
        {
          'detail':
          'Unfollow realizado.'
        }
      )

    Follow.objects.create(
      follower=request.user,
      following=user,
    )

    return Response(
      {
        'detail':
        'Agora você segue este usuário.'
      }
    )
  
class FollowersListView(
  APIView
):
  def get(
    self,
    request,
    username
  ):
    user = (
      get_object_or_404(
        User,
        username=username
      )
    )

    followers = [
      item.follower
      for item
      in user.follower_relationships.all()
    ]

    serializer = (
      UserPublicSerializer(
        followers,
        many=True
      )
    )

    return Response(
      serializer.data
    )
  
class FollowingListView(
  APIView
):
  def get(
    self,
    request,
    username
  ):
    user = (
      get_object_or_404(
        User,
        username=username
      )
    )

    following = [
      item.following
      for item
      in user.following_relationships.all()
    ]

    serializer = (
      UserPublicSerializer(
        following,
        many=True
      )
    )

    return Response(
      serializer.data
    )
  
class LoginView(
  TokenObtainPairView
):
  throttle_classes = [
    LoginRateThrottle
  ]