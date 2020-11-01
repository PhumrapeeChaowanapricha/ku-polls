
import datetime
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0007_auto_20201030_2128'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserVote',
            new_name='Vote',
        ),
        migrations.AlterField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 31, 15, 8, 37, 306301, tzinfo=utc), verbose_name='date end'),
        ),
    ]