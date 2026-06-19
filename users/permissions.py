from rest_framework.permissions import (
  BasePermission,
)

from friendships.models import (
  Follow,
)

class IsProfilePublicOrFriend(
  BasePermission
):
  def has_object_permission(
    self,
    request,
    view,
    obj
  ):
    if not obj.is_private:
      return True
    
    if (
      request.user.is_authenticated
      and request.user == obj
    ):
      return True
    
    if (
      request.user.is_authenticated
      and request.user.role == 'ADMIN'
    ):
      return True
    
    if not request.user.is_authenticated:
      return False

    return Follow.objects.filter(
      follower=request.user,
      following=obj,
    ).exists()