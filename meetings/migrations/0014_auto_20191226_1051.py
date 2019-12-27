# Generated by Django 2.2.7 on 2019-12-26 10:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0013_auto_20191226_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='participants',
            field=models.ManyToManyField(default=[], related_name='meeting_participants', to=settings.AUTH_USER_MODEL),
        ),
    ]