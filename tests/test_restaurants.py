import pytest

@pytest.mark.django_db
def test_admin_can_create_restaurant(auth_client_admin):
    payload = {"name": "THE GOOD BURGERS", "opening_hours": "09:00-23:00"}
    response = auth_client_admin.post("/api/restaurants/", payload, format="json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_employee_cannot_create_restaurant(auth_client_employee):
    payload = {"name": "THE GOOD BURGERS", "opening_hours": "09:00-23:00"}
    response = auth_client_employee.post("/api/restaurants/", payload, format="json")
    assert response.status_code in (403, 401)


@pytest.mark.django_db
def test_list_restaurants(auth_client_employee):
    response = auth_client_employee.get('/api/restaurants/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_unauthenticated_cannot_list_restaurants(api_client):
    response = api_client.get('/api/restaurants/')
    assert response.status_code == 401
