import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError


@pytest.fixture
def superuser_env(monkeypatch):
    monkeypatch.setenv('DJANGO_SUPERUSER_USERNAME', 'boss')
    monkeypatch.setenv('DJANGO_SUPERUSER_PASSWORD', 'S3cure-pass-91')
    monkeypatch.setenv('DJANGO_SUPERUSER_EMAIL', 'boss@example.com')
    return monkeypatch


@pytest.mark.django_db
def test_ensure_admin_creates_superuser(superuser_env):
    call_command('ensure_admin')

    user = User.objects.get(username='boss')
    assert user.is_superuser
    assert user.is_staff
    assert user.email == 'boss@example.com'
    assert user.check_password('S3cure-pass-91')


@pytest.mark.django_db
def test_ensure_admin_is_idempotent(superuser_env):
    call_command('ensure_admin')
    superuser_env.setenv('DJANGO_SUPERUSER_PASSWORD', 'another-pass-77')
    call_command('ensure_admin')

    assert User.objects.filter(username='boss').count() == 1
    assert User.objects.get(username='boss').check_password('S3cure-pass-91')


@pytest.mark.django_db
def test_ensure_admin_requires_credentials(monkeypatch):
    monkeypatch.delenv('DJANGO_SUPERUSER_USERNAME', raising=False)
    monkeypatch.delenv('DJANGO_SUPERUSER_PASSWORD', raising=False)

    with pytest.raises(CommandError):
        call_command('ensure_admin')
