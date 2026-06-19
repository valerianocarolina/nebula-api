import pytest

from posts.models import Post

from friendships.models import Follow

@pytest.mark.django_db
def test_register_creates_user_and_returns_tokens(
  api_client
):
  response = api_client.post(
    '/api/v1/auth/register/',
    {
      'username': 'testuser',
      'email': 'testuser@email.com',
      'password': 'Senha@123',
      'password_confirm': 'Senha@123',
    },
    format='json'
  )

  assert response.status_code == 201

  assert 'access' in response.data
  assert 'refresh' in response.data

  assert response.data['username'] == 'testuser'

@pytest.mark.django_db
def test_protected_endpoint_requires_authentication(
  api_client
):
  response = api_client.get(
    '/api/v1/users/me/'
  )

  assert response.status_code == 401

@pytest.mark.django_db
def test_common_user_cannot_access_admin_reports(
    authenticated_client,
):
  response = authenticated_client.get(
    '/api/v1/admin/reports/'
  )

  assert response.status_code == 403

@pytest.mark.django_db
def test_admin_can_access_reports_panel(
    admin_client
):
  response = admin_client.get(
    '/api/v1/admin/reports/'
  )

  assert response.status_code == 200

@pytest.mark.django_db
def test_private_posts_not_visible_to_non_followers(
  api_client,
  user_factory,
):
  private_user = user_factory(
    username='rosi',
    is_private=True,
  )

  Post.objects.create(
    author=private_user,
    text='Post privado',
  )

  stranger = user_factory(
    username='carol2'
  )

  api_client.force_authenticate(
    user=stranger
  )

  response = api_client.get(
    '/api/v1/posts/feed/'
  )

  assert response.status_code == 200

  posts = response.data['results']

  assert len(posts) == 0

@pytest.mark.django_db
def test_private_posts_visible_to_followers(
  api_client,
  user_factory,
):
  private_user = user_factory(
    username='rosi',
    is_private=True,
  )

  follower = user_factory(
    username='tulio'
  )

  Follow.objects.create(
    follower=follower,
    following=private_user,
  )

  Post.objects.create(
    author=private_user,
    text='Post privado',
  )

  api_client.force_authenticate(
    user=follower
  )

  response = api_client.get(
    '/api/v1/posts/feed/'
  )

  assert response.status_code == 200

  posts = response.data['results']

  assert len(posts) == 1

  assert (
    posts[0]['text']
    == 'Post privado'
  )