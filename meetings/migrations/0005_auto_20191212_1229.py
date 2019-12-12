# Generated by Django 3.0 on 2019-12-12 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0004_delete_roomsreserved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='name',
        ),
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=models.EmailField(default=None, max_length=254),
        ),
    ]
