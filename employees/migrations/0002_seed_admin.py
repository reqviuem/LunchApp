from django.db import migrations
from django.contrib.auth.hashers import make_password


def seed_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.get_or_create(
        username='admin',
        defaults={
            'password': make_password('12345'),
            'is_superuser': True,
            'is_staff': True,
            'is_active': True,
            'email': 'admin@example.com',
            'first_name': '',
            'last_name': '',
        }
    )


def unseed_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='admin').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_admin, unseed_admin),
    ]