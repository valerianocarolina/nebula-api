from rest_framework import serializers

from chat.models import (
  Conversation,
  Message,
)

from users.serializers import (
  UserPublicSerializer,
)

class ManageSerializer(
  serializers.ModelSerializer
):
  sender = UserPublicSerializer(
    read_only=True
  )

  class Meta:
    model = Message

    fields = (
      'id',
      'sender',
      'text',
      'created_at',
      'is_read',
    )

    read_only_fields = (
      'created_at',
    )

class ConversationSerializer(
    serializers.ModelSerializer
):
  participants = (
    UserPublicSerializer(
      many=True,
      read_only=True
    )
  )

  last_message = (
    serializers.SerializerMethodField()
  )

  unread_count = (
    serializers.SerializerMethodField()
  )

  class Meta:
    model = Conversation

    fields = (
      'id',
      'participants',
      'created_at',
      'last_message',
      'unread_count',
    )

  def get_last_message(
    self,
    obj
  ):
    last_message = (
      obj.messages
      .order_by(
        '-created_at'
      )
      .first()
    )

    if not last_message:
      return None

    return MessageSerializer(
      last_message,
      context=self.context
    ).data

  def get_unread_count(
    self,
    obj
  ):
    request = self.context.get(
      'request'
    )

    if not request:
      return 0

    return (
      obj.messages
      .filter(
        is_read=False
      )
      .exclude(
        sender=request.user
      )
      .count()
    )

class MessageCreateSerializer(
  serializers.ModelSerializer
):
  class Meta:
    model = Message

    fields = (
      'text',
    )

class MessageSerializer(
  serializers.ModelSerializer
):
  sender = UserPublicSerializer(
    read_only=True
  )

  class Meta:
    model = Message

    fields = (
      'id',
      'sender',
      'text',
      'created_at',
      'is_read',
    )

    read_only_fields = (
      'created_at',
    )