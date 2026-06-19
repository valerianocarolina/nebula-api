from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from friendships.models import Follow

from chat.models import (
  Conversation,
  Message,
)

from chat.serializers import (
  ConversationSerializer,
  MessageSerializer,
  MessageCreateSerializer,
)

User = get_user_model()

class ConversationViewSet(
  viewsets.ViewSet
):
  permission_classes = [
    IsAuthenticated
  ]

  def create(
    self,
    request
  ):
    other_user = get_object_or_404(
      User,
      pk=request.data.get(
        'user_id'
      )
    )

    if other_user == request.user:
      return Response(
        {
          'detail':
          'Você não pode conversar consigo mesmo.'
        },
        status=status.HTTP_400_BAD_REQUEST
      )
    
    follows_other = Follow.objects.filter(
      follower=request.user,
      following=other_user,
    ).exists()

    followed_back = Follow.objects.filter(
      follower=other_user,
      following=request.user,
    ).exists()

    if not (
      follows_other
      and followed_back
    ):
      return Response(
        {
          'detail':
          'Os usuários precisam se seguir mutuamente.'
        },
        status=status.HTTP_400_BAD_REQUEST
      )
    
    conversations = (
      Conversation.objects.filter(
        participants=request.user
      )
    )

    for conversation in conversations:
      participants = (
        conversation.participants.all()
      )

      if (
        participants.count() == 2
        and other_user in participants
      ):
        serializer = (
          ConversationSerializer(
            conversation,
            context={
              'request': request
            }
          )
        )

        return Response(
          serializer.data
        )
      
    conversation = (
      Conversation.objects.create()
    )

    conversation.participants.add(
      request.user,
      other_user,
    )

    serializer = (
      ConversationSerializer(
        conversation,
        context={
          'request': request
        }
      )
    )

    return Response(
      serializer.data,
      status=status.HTTP_201_CREATED
    )
    
  def list(
    self,
    request
  ):
    conversations = (
      Conversation.objects
      .filter(
        participants=request.user
      )
      .prefetch_related(
        'participants',
        'messages',
      )
    )

    serializer = (
      ConversationSerializer(
        conversations,
        many=True,
        context={
          'request': request
        }
      )
    )

    return Response(
      serializer.data
    )
    
  @action(
    detail=True,
    methods=['get', 'post'],
    url_path='messages',
  )
  def messages(
    self,
    request,
    pk=None
  ):
    conversation = (
      get_object_or_404(
        Conversation,
        pk=pk
      )
    )

    if not conversation.participants.filter(
      pk=request.user.pk
    ).exists():
      return Response(
        {
          'detail':
          'Você não participa desta conversa.'
        },
        status=status.HTTP_403_FORBIDDEN,
      )
      
    if request.method == 'GET':
      conversation.messages.filter(
        is_read=False
      ).exclude(
        sender=request.user
      ).update(
        is_read=True
      )

      serializer = (
        MessageSerializer(
          conversation.messages.all(),
          many=True,
        )
      )

      return Response(
        serializer.data
      )
      
    serializer = (
      MessageCreateSerializer(
        data=request.data
      )
    )

    serializer.is_valid(
      raise_exception=True
    )

    message = serializer.save(
      sender=request.user,
      conversation=conversation,
    )

    return Response(
      MessageSerializer(
        message
      ).data,
      status=status.HTTP_201_CREATED,
    )