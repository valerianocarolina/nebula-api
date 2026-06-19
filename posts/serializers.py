from rest_framework import serializers

from posts.models import (
  Post,
  PostMedia,
  Tag,
)

from users.serializers import (
  UserPublicSerializer,
)

class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag

    fields = (
      'id',
      'name',
    )

class PostMediaSerializer(serializers.ModelSerializer):
  class Meta:
    model = PostMedia

    fields = (
      'id',
      'file',
      'media_type',
    )

class PostSerializer(serializers.ModelSerializer):
  
  author = UserPublicSerializer(
    read_only=True
  )

  medias = PostMediaSerializer(
    many=True,
    read_only=True
  )

  tags = TagSerializer(
    many=True,
    read_only=True
  )

  reactions_count = serializers.SerializerMethodField()
  comments_count = serializers.SerializerMethodField()

  class Meta:
    model = Post

    fields = (
      'id',
      'author',
      'text',
      'medias',
      'tags',
      'created_at',
      'reactions_count',
      'comments_count',
    )

  def get_reactions_count(self, instance):
    return instance.reactions.count()

  def get_comments_count(self, instance):
    return instance.comments.count()

class PostCreateSerializer(serializers.ModelSerializer):
  media_files = serializers.ListField(
    child=serializers.FileField(),
    required=False,
    write_only=True,
  )

  class Meta:
    model = Post

    fields = (
      'text',
      'media_files',
    )

  def create(self, validated_data):
    validated_data.pop(
      'media_files',
      None
    )

    return Post.objects.create(
      **validated_data
    )