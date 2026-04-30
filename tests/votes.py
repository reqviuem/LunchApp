import pytest

@pytest.mark.django_db
def test_employee_can_vote(auth_client_employee, menu):
    response = auth_client_employee.post('/api/votes/', {'menu': menu.id})
    assert response.status_code == 201

@pytest.mark.django_db
def test_employee_cannot_vote_twice(auth_client_employee, menu):
    auth_client_employee.post('/api/votes/', {'menu': menu.id})
    response = auth_client_employee.post('/api/votes/', {'menu': menu.id})
    assert response.status_code == 400