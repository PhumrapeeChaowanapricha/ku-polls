import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0006_auto_20201030_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='user',
        ),
        migrations.AddField(
            model_name='question',
            name='previous_vote',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 31, 14, 28, 10, 948920, tzinfo=utc), verbose_name='date end'),
        ),
        migrations.CreateModel(
            name='UserVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
