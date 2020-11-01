import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20201030_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 31, 15, 13, 52, 193779, tzinfo=utc), verbose_name='date end'),
        ),
    ]