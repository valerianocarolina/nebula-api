from rest_framework.routers import DefaultRouter

from chat.views import (
  ConversationViewSet,
)

router = DefaultRouter()

router.register(
  '',
  ConversationViewSet,
  basename='conversations',
)

urlpatterns = router.urls