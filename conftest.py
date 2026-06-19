import pytest
import factory

from rest_framework.test import APIClient

from users.models import CustomUser

@pytest.fixture
def api_client():
  return APIClient()

class UserFactory(
  factory.django.DjangoModelFactory
):
  class Meta:
    model = CustomUser

  username = factory.Sequence(
    lambda n: f'user{n}'
  )

  email = factory.LazyAttribute(
    lambda obj:
    f'{obj.username}@email.com'
  )

  role = 'COMMON'

class AdminFactory(
  factory.django.DjangoModelFactory
):
  class Meta:
    model = CustomUser

  username = factory.Sequence(
    lambda n: f'admin{n}'
  )

  email = factory.LazyAttribute(
    lambda obj:
    f'{obj.username}@email.com'
  )

  role = 'ADMIN'

@pytest.fixture
def user_factory():
  return UserFactory

@pytest.fixture
def admin_factory():
  return AdminFactory

@pytest.fixture
def user(db):
  return UserFactory()

@pytest.fixture
def admin(db):
  return AdminFactory()

@pytest.fixture
def authenticated_client(
  db,
  api_client,
  user
):
  api_client.force_authenticate(
    user=user
  )

  return api_client

@pytest.fixture
def admin_client(
  db,
  api_client,
  admin
):
  api_client.force_authenticate(
    user=admin
  )

  return api_client

