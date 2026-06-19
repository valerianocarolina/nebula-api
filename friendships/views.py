from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from friendships.models import (
  FriendRequest,
  Follow,
)

from friendships.serializers import (
  FriendRequestSerializer,
)

User = get_user_model()

class FriendRequestViewSet(
  viewsets.ViewSet
):
  permission_classes = [
    IsAuthenticated,
  ]

  def list(
      self,
      request
  ):
    requests = (
      FriendRequest.objects
      .filter(
        receiver=request.user,
        status=FriendRequest.Status.PENDING,
      )
    )

    serializer = (
      FriendRequestSerializer(
        requests,
        many=True
      )
    )

    return Response(
      serializer.data
    )
  
  def create(
    self,
    request
  ):
    receiver = get_object_or_404(
      User,
      pk=request.data.get(
        'receiver_id'
      )
    )

    if receiver == request.user:
      return Response(
        {
          'detail':
          'Você não pode enviar amizade para si mesmo.'
        },
        status=status.HTTP_400_BAD_REQUEST
      )

    existing_request = FriendRequest.objects.filter(
      sender=request.user,
      receiver=receiver,
    ).first()

    if existing_request:
      return Response(
        {
          'detail':
          'Já existe uma solicitação para este usuário.'
        },
        status=status.HTTP_400_BAD_REQUEST
      )

    friendship = FriendRequest.objects.create(
      sender=request.user,
      receiver=receiver,
    )

    serializer = FriendRequestSerializer(
      friendship
    )

    return Response(
      serializer.data,
      status=status.HTTP_201_CREATED
    )
  
  def partial_update(
    self,
    request,
    pk=None
  ):
    friendship = (
      get_object_or_404(
        FriendRequest,
        pk=pk,
        receiver=request.user,
      )
    )

    status_value = (
      request.data.get(
        'status'
      )
    )

    if status_value not in [
      FriendRequest.Status.ACCEPTED,
      FriendRequest.Status.REJECTED,
    ]:
      return Response(
       {
         'detail':
         'Status inválido.'
       },
       status=400
      )
    
    friendship.status = (
      status_value
    )

    friendship.save()

    if (
      status_value
      ==
      FriendRequest.Status.ACCEPTED
    ):
      Follow.objects.get_or_create(
        follower=friendship.sender,
        following=friendship.receiver,
      )

    serializer = (
      FriendRequestSerializer(
        friendship
      )
    )

    return Response(
      serializer.data
    )