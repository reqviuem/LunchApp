import pytest

from myproject.throttles import LoginRateThrottle, RegistrationRateThrottle


@pytest.mark.django_db
def test_login_is_throttled(api_client, monkeypatch):
    monkeypatch.setitem(LoginRateThrottle.THROTTLE_RATES, 'login', '2/min')
    payload = {'username': 'nobody', 'password': 'wrong'}

    statuses = [api_client.post('/api/token/', payload, format='json').status_code for _ in range(3)]

    assert statuses == [401, 401, 429]


@pytest.mark.django_db
def test_registration_is_throttled(api_client, monkeypatch):
    monkeypatch.setitem(RegistrationRateThrottle.THROTTLE_RATES, 'register', '2/hour')

    statuses = [api_client.post('/api/employees/', {}, format='json').status_code for _ in range(3)]

    assert statuses == [400, 400, 429]


@pytest.mark.django_db
def test_authenticated_api_calls_are_not_throttled_like_login(auth_client_employee, monkeypatch):
    monkeypatch.setitem(LoginRateThrottle.THROTTLE_RATES, 'login', '1/min')

    statuses = [auth_client_employee.get('/api/restaurants/').status_code for _ in range(3)]

    assert statuses == [200, 200, 200]
