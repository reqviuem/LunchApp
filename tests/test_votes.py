from datetime import timedelta

import pytest
from django.utils import timezone

from tests.factories import MenuFactory, VoteFactory
from voting.models import Vote

VOTE_URL = '/api/voting/vote/'


@pytest.mark.django_db
def test_employee_can_vote(auth_client_employee, employee_user, menu):
    response = auth_client_employee.post(VOTE_URL, {'menu': menu.id}, format='json')

    assert response.status_code == 201
    vote = Vote.objects.get()
    assert vote.employee == employee_user
    assert vote.menu == menu
    assert vote.date == timezone.localdate()


@pytest.mark.django_db
def test_employee_cannot_vote_twice_for_same_menu(auth_client_employee, menu):
    auth_client_employee.post(VOTE_URL, {'menu': menu.id}, format='json')
    response = auth_client_employee.post(VOTE_URL, {'menu': menu.id}, format='json')

    assert response.status_code == 400
    assert Vote.objects.count() == 1


@pytest.mark.django_db
def test_employee_cannot_vote_for_two_menus_on_the_same_day(auth_client_employee, menu):
    other_menu = MenuFactory()
    auth_client_employee.post(VOTE_URL, {'menu': menu.id}, format='json')
    response = auth_client_employee.post(VOTE_URL, {'menu': other_menu.id}, format='json')

    assert response.status_code == 400
    assert Vote.objects.count() == 1


@pytest.mark.django_db
def test_employee_cannot_vote_for_menu_of_another_day(auth_client_employee):
    old_menu = MenuFactory(date=timezone.localdate() - timedelta(days=1))
    response = auth_client_employee.post(VOTE_URL, {'menu': old_menu.id}, format='json')

    assert response.status_code == 400
    assert Vote.objects.count() == 0


@pytest.mark.django_db
def test_employee_can_vote_again_on_a_new_day(auth_client_employee, employee_user, menu):
    old_menu = MenuFactory(date=timezone.localdate() - timedelta(days=1))
    VoteFactory(employee=employee_user, menu=old_menu)

    response = auth_client_employee.post(VOTE_URL, {'menu': menu.id}, format='json')

    assert response.status_code == 201
    assert Vote.objects.filter(employee=employee_user).count() == 2


@pytest.mark.django_db
def test_vote_for_unknown_menu_is_rejected(auth_client_employee):
    response = auth_client_employee.post(VOTE_URL, {'menu': 999999}, format='json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_user_without_employee_profile_cannot_vote(auth_client_admin, menu):
    response = auth_client_admin.post(VOTE_URL, {'menu': menu.id}, format='json')

    assert response.status_code == 403
    assert Vote.objects.count() == 0


@pytest.mark.django_db
def test_unauthenticated_cannot_vote(api_client, menu):
    response = api_client.post(VOTE_URL, {'menu': menu.id}, format='json')

    assert response.status_code == 401
