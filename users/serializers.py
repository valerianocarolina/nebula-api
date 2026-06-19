from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from users.models import CustomUser
from friendships.models import Follow

class UserPublicSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser

    fields = (
      'id',
      'username',
      'avatar',
      'bio',
      'is_private',
    )

class UserDetailSerializer(serializers.ModelSerializer):
  followers_count = serializers.SerializerMethodField()
  following_count = serializers.SerializerMethodField()

  class Meta:
    model = CustomUser

    fields = (
      'id',
      'username',
      'email',
      'avatar',
      'bio',
      'is_private',
      'role',
      'followers_count',
      'following_count',
    )

    read_only_fields = [
      'id',
      'username',
      'email',
      'followers_count',
      'following_count',
    ]

  def get_followers_count(self, obj):
    return Follow.objects.filter(following=obj).count()

  def get_following_count(self, obj):
    return Follow.objects.filter(follower=obj).count()

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(
    write_only=True,
    required=True
  )

  password_confirm = serializers.CharField(
    write_only=True,
    required=True
  )

  class Meta:
    model = CustomUser

    fields = (
      'username',
      'email',
      'password',
      'password_confirm'
    )

  def validate(self, attrs):
    password = attrs.get('password')
    password_confirm = attrs.get('password_confirm')

    if password != password_confirm:
      raise serializers.ValidationError(
        {
          'password_confirm':
          'As senhas não coincidem.'
        }
      )

    validate_password(password)

    return attrs

  def validate_email(self, value):
    if CustomUser.objects.filter(
      email=value
    ).exists():

      raise serializers.ValidationError(
        'Este e-mail já está em uso.'
      )

    return value


  def create(self, validated_data):
    validated_data.pop('password_confirm')

    user = CustomUser(
      username=validated_data['username'],
      email=validated_data['email'],
    )

    user.set_password(
      validated_data['password']
    )

    user.save()

    return user


class ChangePasswordSerializer(serializers.Serializer):
  old_password = serializers.CharField(
    required=True,
    write_only=True
  )

  new_password = serializers.CharField(
    required=True,
    write_only=True
  )

  def validate_new_password(self, value):
    validate_password(value)
    return value

class LogoutSerializer(
  serializers.Serializer
):
  refresh = serializers.CharField()