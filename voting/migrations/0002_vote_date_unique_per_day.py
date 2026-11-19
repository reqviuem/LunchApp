from django.db import migrations, models


def copy_menu_date(apps, schema_editor):
    Vote = apps.get_model('voting', 'Vote')
    for vote in Vote.objects.select_related('menu'):
        vote.date = vote.menu.date
        vote.save(update_fields=['date'])


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.RunPython(copy_menu_date, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='vote',
            name='date',
            field=models.DateField(),
        ),
        migrations.RemoveConstraint(
            model_name='vote',
            name='unique_vote_per_menu',
        ),
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.UniqueConstraint(fields=('employee', 'date'), name='unique_vote_per_employee_per_day'),
        ),
    ]
