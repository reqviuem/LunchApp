from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone

from restaurants.models import Menu, MenuItem
from tests.factories import MenuFactory, MenuItemFactory

MENUS_URL = '/api/restaurants/menus/'
TODAY_URL = '/api/restaurants/menus/today/'


@pytest.mark.django_db
def test_admin_can_create_menu(auth_client_admin, restaurant):
    payload = {"restaurant": restaurant.id, "date": "2025-12-06", "title": "Burger Day"}
    response = auth_client_admin.post(MENUS_URL, payload, format="json")

    assert response.status_code == 201
    assert Menu.objects.get().title == "Burger Day"


@pytest.mark.django_db
def test_admin_can_create_menu_with_items(auth_client_admin, restaurant):
    payload = {
        "restaurant": restaurant.id,
        "date": "2025-12-06",
        "title": "Burger Day",
        "items": [
            {"name": "Cheeseburger", "price": "8.50"},
            {"name": "Fries", "price": "3.00"},
        ],
    }
    response = auth_client_admin.post(MENUS_URL, payload, format="json")

    assert response.status_code == 201
    assert [item["name"] for item in response.json()["items"]] == ["Cheeseburger", "Fries"]
    assert MenuItem.objects.filter(menu__title="Burger Day").count() == 2


@pytest.mark.django_db
def test_menu_item_with_negative_price_is_rejected(auth_client_admin, restaurant):
    payload = {
        "restaurant": restaurant.id,
        "date": "2025-12-06",
        "title": "Burger Day",
        "items": [{"name": "Cheeseburger", "price": "-1.00"}],
    }
    response = auth_client_admin.post(MENUS_URL, payload, format="json")

    assert response.status_code == 400
    assert Menu.objects.count() == 0


@pytest.mark.django_db
def test_restaurant_cannot_have_two_menus_on_the_same_day(auth_client_admin, menu):
    payload = {"restaurant": menu.restaurant.id, "date": menu.date.isoformat(), "title": "Second"}
    response = auth_client_admin.post(MENUS_URL, payload, format="json")

    assert response.status_code == 400
    assert Menu.objects.count() == 1


@pytest.mark.django_db
def test_employee_cannot_create_menu(auth_client_employee, restaurant):
    payload = {"restaurant": restaurant.id, "date": "2025-12-06", "title": "Burger Day"}
    response = auth_client_employee.post(MENUS_URL, payload, format="json")

    assert response.status_code == 403
    assert Menu.objects.count() == 0


@pytest.mark.django_db
def test_today_menus_are_empty_without_menus(auth_client_employee):
    response = auth_client_employee.get(TODAY_URL)

    assert response.status_code == 200
    assert response.json()["results"] == []


@pytest.mark.django_db
def test_today_menus_return_only_todays_menus_with_items(auth_client_employee, menu):
    MenuItemFactory(menu=menu, name="Margherita", price=Decimal("7.00"))
    MenuFactory(date=timezone.localdate() - timedelta(days=1))
    MenuFactory(date=timezone.localdate() + timedelta(days=1))

    response = auth_client_employee.get(TODAY_URL)

    assert response.status_code == 200
    results = response.json()["results"]
    assert [entry["id"] for entry in results] == [menu.id]
    assert results[0]["items"] == [{"id": results[0]["items"][0]["id"], "name": "Margherita", "price": "7.00"}]


@pytest.mark.django_db
def test_unauthenticated_cannot_list_menus(api_client):
    response = api_client.get(TODAY_URL)

    assert response.status_code == 401
