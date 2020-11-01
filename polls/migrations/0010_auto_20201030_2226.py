import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20201030_2213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vote',
            old_name='choice',
            new_name='selected_choice',
        ),
        migrations.AlterField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 31, 15, 26, 40, 858191, tzinfo=utc), verbose_name='date end'),
        ),
    ]