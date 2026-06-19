from rest_framework import serializers
from comments.models import Comment
from users.serializers import (
  UserPublicSerializer,
)

class CommentReplySerializer(serializers.ModelSerializer):

  author = UserPublicSerializer(
    read_only=True
  )

  class Meta:
    model = Comment

    fields = (
      'id',
      'author',
      'text',
      'created_at',
    )

class CommentSerializer(serializers.ModelSerializer):

  author = UserPublicSerializer(
    read_only=True
  )

  replies = serializers.SerializerMethodField()

  class Meta:
    model = Comment

    fields = (
      'id',
      'author',
      'text',
      'created_at',
      'replies',
    )

  def get_replies(self, obj):
    replies = obj.replies.all()

    return CommentReplySerializer(
      replies,
      many=True,
    ).data

class CommentCreateSerializer(
  serializers.ModelSerializer
):
  class Meta:
    model = Comment

    fields = (
      'text',
      'parent',
    )