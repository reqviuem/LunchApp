from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0002_vote_date_unique_per_day'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='vote',
            index=models.Index(fields=['date'], name='vote_date_idx'),
        ),
    ]
