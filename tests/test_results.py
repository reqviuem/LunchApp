from datetime import timedelta

import pytest
from django.utils import timezone

from tests.factories import MenuFactory, VoteFactory

RESULTS_URL = '/api/voting/results/today/'


@pytest.mark.django_db
def test_results_are_empty_when_nobody_voted(auth_client_employee):
    response = auth_client_employee.get(RESULTS_URL)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_results_are_ordered_by_votes(auth_client_employee):
    popular = MenuFactory(title='Popular')
    quiet = MenuFactory(title='Quiet')
    VoteFactory.create_batch(3, menu=popular)
    VoteFactory(menu=quiet)

    response = auth_client_employee.get(RESULTS_URL)

    assert response.status_code == 200
    assert response.json() == [
        {'menu_id': popular.id, 'menu_title': 'Popular', 'restaurant': popular.restaurant.name, 'votes': 3},
        {'menu_id': quiet.id, 'menu_title': 'Quiet', 'restaurant': quiet.restaurant.name, 'votes': 1},
    ]


@pytest.mark.django_db
def test_results_ignore_votes_from_previous_days(auth_client_employee):
    old_menu = MenuFactory(date=timezone.localdate() - timedelta(days=1))
    VoteFactory.create_batch(2, menu=old_menu)

    response = auth_client_employee.get(RESULTS_URL)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_results_require_authentication(api_client):
    response = api_client.get(RESULTS_URL)

    assert response.status_code == 401
