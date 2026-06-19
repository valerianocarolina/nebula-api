from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from reports.models import Report

from posts.models import Post
from users.models import CustomUser

from users.serializers import (
  UserPublicSerializer,
)

class ReportSerializer(
  serializers.ModelSerializer
):
  content_type = serializers.CharField(
    write_only=True
  )

  reporter = UserPublicSerializer(
    read_only=True
  )

  reported_object = serializers.SerializerMethodField()

  class Meta:
    model = Report

    fields = (
      'id',
      'reporter',
      'content_type',
      'object_id',
      'reported_object',
      'reason',
      'status',
      'created_at',
    )

    read_only_fields = (
      'status',
      'created_at',
      'reporter',
      'reported_object',
    )

  def validate_content_type(
    self,
    value
  ):
    value = value.lower()

    mapping = {
      'post': Post,
      'user': CustomUser,
    }

    if value not in mapping:
      raise serializers.ValidationError(
        'Tipo inválido. Use post ou user.'
      )
    
    return ContentType.objects.get_for_model(
      mapping[value]
    )
  
  def validate(
    self,
    attrs
  ):
    model_class = (
      attrs['content_type']
      .model_class()
    )

    exists = model_class.objects.filter(
      id=attrs['object_id']
    ).exists()

    if not exists:
      raise serializers.ValidationError(
        {
          'object_id':
          'Objeto não encontrado.'
        }
      )
    
    return attrs
  
  def get_reported_object(
    self,
    obj
  ):
    target = obj.reported_object

    if target is None:
      return None

    if isinstance(
      target,
      Post
    ):
      return {
        'id': target.id,
        'type': 'post',
        'content': target.text,
      }
    
    if isinstance(
      target,
      CustomUser
    ):
      return {
        'id': target.id,
        'type': 'user',
        'username': target.username,
      }
    
    return None