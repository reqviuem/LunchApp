import pytest

@pytest.mark.django_db
def test_admin_can_create_menu(auth_client_admin, restaurant):
    payload = {"restaurant": restaurant.id, "date": "2025-12-06", "title": "Burger Day"}
    response = auth_client_admin.post("/api/menus/", payload, format="json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_employee_cannot_create_menu(auth_client_employee, restaurant):
    payload = {"restaurant": restaurant.id, "date": "2025-12-06", "title": "Burger Day"}
    response = auth_client_employee.post("/api/menus/", payload, format="json")
    assert response.status_code in (403, 401)


@pytest.mark.django_db
def test_list_menus(auth_client_employee):
    response = auth_client_employee.get('/api/menus/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_unauthenticated_cannot_list_menus(api_client):
    response = api_client.get('/api/menus/')
    assert response.status_code == 401
