# Generated by Django 2.2.7 on 2019-12-02 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0002_meeting_is_cancelled'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomsReserved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]
