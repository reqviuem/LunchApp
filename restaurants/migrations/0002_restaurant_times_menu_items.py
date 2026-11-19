import datetime

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='restaurant',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='restaurant',
            name='opening_time',
            field=models.TimeField(default=datetime.time(9, 0)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='closing_time',
            field=models.TimeField(default=datetime.time(18, 0)),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='opening_hours',
        ),
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ['-date', 'restaurant__name']},
        ),
        migrations.AddIndex(
            model_name='menu',
            index=models.Index(fields=['date'], name='menu_date_idx'),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)])),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='restaurants.menu')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
