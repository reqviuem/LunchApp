import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient

from employees.models import Employee
from restaurants.models import Restaurant, Menu


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    user = User.objects.create_superuser(username='admin', password='admin123')
    return user


@pytest.fixture
def employee_user():
    user = User.objects.create_user(username='alice', password='test1234')
    employee = Employee.objects.create(user=user, name='Alice')
    return employee


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
    return Restaurant.objects.create(name='Pizza Place', opening_hours='10:00-18:00')


@pytest.fixture
def menu(restaurant):
    today = timezone.now().date()
    return Menu.objects.create(restaurant=restaurant, date=today, title='Pizza Day')