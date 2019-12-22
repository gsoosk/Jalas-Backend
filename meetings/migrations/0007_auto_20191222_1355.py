# Generated by Django 3.0 on 2019-12-22 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0006_auto_20191222_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='username',
        ),
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]