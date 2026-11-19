import pytest


@pytest.mark.django_db
def test_schema_is_public_and_describes_the_api(api_client):
    response = api_client.get('/api/schema/')

    assert response.status_code == 200
    body = response.content.decode()
    assert 'LunchApp API' in body
    assert '/api/restaurants/{id}/' in body
    assert '/api/voting/results/today/' in body


@pytest.mark.django_db
@pytest.mark.parametrize('url', ['/api/docs/', '/api/redoc/'])
def test_documentation_pages_are_public(api_client, url):
    response = api_client.get(url)

    assert response.status_code == 200
