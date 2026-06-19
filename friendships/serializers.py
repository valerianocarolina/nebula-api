from django.contrib.auth import get_user_model

from rest_framework import serializers

from friendships.models import FriendRequest

from users.serializers import (
    UserPublicSerializer,
)

User = get_user_model()

class FriendRequestCreateSerializer(
    serializers.ModelSerializer
):

    receiver = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = FriendRequest

        fields = (
            'receiver',
        )

class FriendRequestSerializer(
    serializers.ModelSerializer
):

    sender = UserPublicSerializer(
        read_only=True
    )

    receiver = UserPublicSerializer(
        read_only=True
    )

    class Meta:
        model = FriendRequest

        fields = (
            'id',
            'sender',
            'receiver',
            'status',
            'created_at',
        )

class FriendRequestSerializer(
    serializers.ModelSerializer
):

    sender = UserPublicSerializer(
        read_only=True
    )

    receiver = UserPublicSerializer(
        read_only=True
    )

    class Meta:
        model = FriendRequest

        fields = (
            'id',
            'sender',
            'receiver',
            'status',
            'created_at',
        )

class FriendRequestUpdateSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = FriendRequest

        fields = (
            'status',
        )