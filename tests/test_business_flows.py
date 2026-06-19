import pytest

from posts.models import Post
from reactions.models import Reaction
from reports.models import Report
from friendships.models import (
  FriendRequest,
  Follow,
)

from django.contrib.contenttypes.models import (
  ContentType,
)

@pytest.mark.django_db
def test_friendship_request_acceptance_flow(
  api_client,
  user_factory,
):
  sender = user_factory(
    username='tulio'
  )

  receiver = user_factory(
    username='rosi'
  )

  api_client.force_authenticate(
    user=sender
  )

  response = api_client.post(
    '/api/v1/friendships/requests/',
    {
      'receiver_id': receiver.id
    },
    format='json'
  )

  assert response.status_code == 201

  request_id = response.data['id']

  api_client.force_authenticate(
    user=receiver
  )

  response = api_client.patch(
    f'/api/v1/friendships/requests/{request_id}/',
    {
      'status': 'ACCEPTED'
    },
    format='json',
  )

  assert response.status_code == 200

  assert Follow.objects.filter(
    follower=sender,
    following=receiver,
  ).exists()

@pytest.mark.django_db
def test_conversation_requires_mutual_follow(
  api_client,
  user_factory,
):
  user1 = user_factory(
    username='tulio'
  )

  user2 = user_factory(
    username='rosi'
  )

  api_client.force_authenticate(
    user=user1
  )

  response = api_client.post(
    '/api/v1/conversations/',
    {
      'user_id': user2.id
    },
    format='json'
  )

  assert response.status_code == 400

@pytest.mark.django_db
def test_conversation_creation_with_mutual_follow(
  api_client,
  user_factory,
):
  user1 = user_factory()

  user2 = user_factory()

  Follow.objects.create(
    follower=user1,
    following=user2,
  )

  Follow.objects.create(
    follower=user2,
    following=user1,
  )

  api_client.force_authenticate(
    user=user1
  )

  response = api_client.post(
    '/api/v1/conversations/',
    {
      'user_id': user2.id
    },
    format='json'
  )

  assert response.status_code == 201

@pytest.mark.django_db
def test_resolved_report_deletes_post(
  admin_client,
  user_factory,
):
  user = user_factory()

  post = Post.objects.create(
    author=user,
    text='Post inadequado',
  )

  report = Report.objects.create(
    reporter=user,
    content_type=ContentType.objects.get_for_model(Post),
    object_id=post.id,
    reason='Spam',
  )

  response = admin_client.patch(
    f'/api/v1/admin/reports/{report.id}/',
    {
      'status': 'RESOLVED',
      'action': 'delete',
    },
    format='json'
  )

  assert response.status_code == 200

  assert not Post.objects.filter(
    id=post.id
  ).exists()

@pytest.mark.django_db
def test_reaction_toggle(
  api_client,
  user_factory,
):
  user = user_factory()

  post = Post.objects.create(
    author=user,
    text='Meu post',
  )

  api_client.force_authenticate(
    user=user
  )

  response = api_client.post(
    f'/api/v1/posts/{post.id}/react/',
  )

  assert response.status_code == 200

  assert Reaction.objects.count() == 1

  response = api_client.post(
    f'/api/v1/posts/{post.id}/react/',
  )

  assert response.status_code == 200

  assert Reaction.objects.count() == 0