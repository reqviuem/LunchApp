import pytest

from restaurants.models import Restaurant
from tests.factories import RestaurantFactory

RESTAURANTS_URL = '/api/restaurants/'
VALID_PAYLOAD = {"name": "THE GOOD BURGERS", "opening_time": "09:00", "closing_time": "23:00"}


@pytest.mark.django_db
def test_admin_can_create_restaurant(auth_client_admin):
    response = auth_client_admin.post(RESTAURANTS_URL, VALID_PAYLOAD, format="json")

    assert response.status_code == 201
    assert Restaurant.objects.get().name == "THE GOOD BURGERS"


@pytest.mark.django_db
@pytest.mark.parametrize('missing', ['name', 'opening_time', 'closing_time'])
def test_create_restaurant_requires_all_fields(auth_client_admin, missing):
    payload = {key: value for key, value in VALID_PAYLOAD.items() if key != missing}

    response = auth_client_admin.post(RESTAURANTS_URL, payload, format="json")

    assert response.status_code == 400
    assert missing in response.json()


@pytest.mark.django_db
def test_employee_cannot_create_restaurant(auth_client_employee):
    response = auth_client_employee.post(RESTAURANTS_URL, VALID_PAYLOAD, format="json")

    assert response.status_code == 403
    assert Restaurant.objects.count() == 0


@pytest.mark.django_db
def test_list_restaurants_is_paginated_and_sorted_by_name(auth_client_employee):
    RestaurantFactory(name="Zeta")
    RestaurantFactory(name="Alpha")

    response = auth_client_employee.get(RESTAURANTS_URL)

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
    assert [entry["name"] for entry in body["results"]] == ["Alpha", "Zeta"]


@pytest.mark.django_db
def test_unauthenticated_cannot_list_restaurants(api_client):
    response = api_client.get(RESTAURANTS_URL)

    assert response.status_code == 401
