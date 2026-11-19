import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create a superuser from DJANGO_SUPERUSER_* environment variables if it does not exist.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')

        if not username or not password:
            raise CommandError('DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD must be set.')

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(f'Superuser "{username}" already exists.')
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created.'))
