import pytest

from restaurants.models import Menu, Restaurant
from tests.factories import MenuFactory, RestaurantFactory


def detail_url(restaurant):
    return f'/api/restaurants/{restaurant.id}/'


@pytest.mark.django_db
def test_employee_can_retrieve_restaurant(auth_client_employee, restaurant):
    response = auth_client_employee.get(detail_url(restaurant))

    assert response.status_code == 200
    assert response.json() == {
        'id': restaurant.id,
        'name': 'Pizza Place',
        'opening_time': '10:00:00',
        'closing_time': '18:00:00',
    }


@pytest.mark.django_db
def test_retrieve_unknown_restaurant_returns_404(auth_client_employee):
    response = auth_client_employee.get('/api/restaurants/999999/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_admin_can_update_restaurant(auth_client_admin, restaurant):
    payload = {'name': 'Pizza Palace', 'opening_time': '11:00', 'closing_time': '22:00'}

    response = auth_client_admin.put(detail_url(restaurant), payload, format='json')

    assert response.status_code == 200
    restaurant.refresh_from_db()
    assert restaurant.name == 'Pizza Palace'
    assert restaurant.closing_time.hour == 22


@pytest.mark.django_db
def test_admin_can_partially_update_restaurant(auth_client_admin, restaurant):
    response = auth_client_admin.patch(detail_url(restaurant), {'name': 'Renamed'}, format='json')

    assert response.status_code == 200
    restaurant.refresh_from_db()
    assert restaurant.name == 'Renamed'
    assert restaurant.opening_time.hour == 10


@pytest.mark.django_db
def test_employee_cannot_update_restaurant(auth_client_employee, restaurant):
    response = auth_client_employee.patch(detail_url(restaurant), {'name': 'Hacked'}, format='json')

    assert response.status_code == 403
    restaurant.refresh_from_db()
    assert restaurant.name == 'Pizza Place'


@pytest.mark.django_db
def test_admin_can_delete_restaurant_with_its_menus(auth_client_admin, restaurant):
    MenuFactory(restaurant=restaurant)

    response = auth_client_admin.delete(detail_url(restaurant))

    assert response.status_code == 204
    assert not Restaurant.objects.filter(id=restaurant.id).exists()
    assert Menu.objects.count() == 0


@pytest.mark.django_db
def test_employee_cannot_delete_restaurant(auth_client_employee, restaurant):
    response = auth_client_employee.delete(detail_url(restaurant))

    assert response.status_code == 403
    assert Restaurant.objects.filter(id=restaurant.id).exists()


@pytest.mark.django_db
def test_unauthenticated_cannot_access_restaurant(api_client):
    restaurant = RestaurantFactory()

    response = api_client.get(detail_url(restaurant))

    assert response.status_code == 401
