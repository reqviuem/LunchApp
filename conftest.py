import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from tests.factories import EmployeeFactory, MenuFactory, RestaurantFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return User.objects.create_superuser(username='admin', password='admin123')


@pytest.fixture
def employee_user():
    return EmployeeFactory(user__username='alice', name='Alice')


@pytest.fixture
def auth_client_employee(api_client, employee_user):
    api_client.force_authenticate(user=employee_user.user)
    return api_client


@pytest.fixture
def auth_client_admin(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def restaurant():
    return RestaurantFactory(name='Pizza Place')


@pytest.fixture
def menu(restaurant):
    return MenuFactory(restaurant=restaurant, title='Pizza Day')
