import pytest
from django.contrib.auth.models import User

from employees.models import Employee
from tests.factories import EmployeeFactory

EMPLOYEES_URL = '/api/employees/'
VALID_PAYLOAD = {'name': 'Bob', 'username': 'bob', 'password': 'S3cure-pass-91'}


@pytest.mark.django_db
def test_employee_created_with_user():
    user = User.objects.create_user(username='vitalik', password='3821')
    employee = Employee.objects.create(user=user, name='Vitalik')

    assert employee.user == user
    assert str(employee) == 'Vitalik'


@pytest.mark.django_db
def test_register_employee(api_client):
    response = api_client.post(EMPLOYEES_URL, VALID_PAYLOAD, format='json')

    assert response.status_code == 201
    assert response.json()['name'] == 'Bob'
    assert 'password' not in response.json()
    employee = Employee.objects.get(user__username='bob')
    assert employee.user.check_password(VALID_PAYLOAD['password'])


@pytest.mark.django_db
def test_registered_employee_can_obtain_token(api_client):
    api_client.post(EMPLOYEES_URL, VALID_PAYLOAD, format='json')

    response = api_client.post(
        '/api/token/',
        {'username': 'bob', 'password': VALID_PAYLOAD['password']},
        format='json',
    )

    assert response.status_code == 200
    assert 'access' in response.json()
    assert 'refresh' in response.json()


@pytest.mark.django_db
def test_register_with_duplicate_username_is_rejected(api_client):
    EmployeeFactory(user__username='bob')

    response = api_client.post(EMPLOYEES_URL, VALID_PAYLOAD, format='json')

    assert response.status_code == 400
    assert 'username' in response.json()
    assert User.objects.filter(username='bob').count() == 1


@pytest.mark.django_db
def test_register_with_weak_password_is_rejected(api_client):
    payload = {**VALID_PAYLOAD, 'password': '123'}

    response = api_client.post(EMPLOYEES_URL, payload, format='json')

    assert response.status_code == 400
    assert 'password' in response.json()
    assert not User.objects.filter(username='bob').exists()


@pytest.mark.django_db
@pytest.mark.parametrize('missing', ['name', 'username', 'password'])
def test_register_requires_all_fields(api_client, missing):
    payload = {key: value for key, value in VALID_PAYLOAD.items() if key != missing}

    response = api_client.post(EMPLOYEES_URL, payload, format='json')

    assert response.status_code == 400
    assert missing in response.json()
