from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from users.views import (
    RegisterView,
    LogoutView,
    LoginView,
)

from .views import (
  FollowToggleView,
  FollowersListView,
  FollowingListView,
  MeView,
  ChangePasswordView,
  UserProfileView,
  UserSearchView,
)

urlpatterns = [
    path(
        'auth/register/',
        RegisterView.as_view(),
        name='register',
    ),

    path(
        'auth/token/',
        LoginView.as_view(),
        name='token_obtain_pair',
    ),

    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),

    path(
        'auth/logout/',
        LogoutView.as_view(),
        name='logout',
    ),

    path(
      'users/me/',
      MeView.as_view(),
      name='me',
    ),

    path(
      'users/me/change-password/',
      ChangePasswordView.as_view(),
      name='change-password',
    ),

    path(
      'users/search/',
      UserSearchView.as_view(),
      name='user-search',
    ),

    path(
      'users/<str:username>/',
      UserProfileView.as_view(),
      name='user-profile',
    ),

    path(
      'users/<str:username>/follow/',
      FollowToggleView.as_view(),
    ),

    path(
      'users/<str:username>/followers/',
      FollowersListView.as_view(),
    ),

    path(
      'users/<str:username>/following/',
      FollowingListView.as_view(),
    )
]