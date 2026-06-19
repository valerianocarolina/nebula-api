from rest_framework.routers import DefaultRouter

from friendships.views import (
  FriendRequestViewSet,
)

router = DefaultRouter()

router.register(
  'requests',
  FriendRequestViewSet,
  basename='friendships'
)

urlpatterns = router.urls