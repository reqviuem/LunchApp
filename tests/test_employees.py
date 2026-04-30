import pytest
from django.contrib.auth.models import User
from employees.models import Employee

@pytest.mark.django_db
def test_employee_created_with_user():
    user = User.objects.create_user(username='vitalik', password='3821')
    employee = Employee.objects.create(user=user, name='Vitalik')
    assert employee.user == user
    assert str(employee.name) == 'Vitalik'