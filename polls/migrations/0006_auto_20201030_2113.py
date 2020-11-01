import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0005_auto_20201030_2037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='user',
        ),
        migrations.AddField(
            model_name='choice',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 31, 14, 13, 39, 544237, tzinfo=utc), verbose_name='date end'),
        ),
    ]
