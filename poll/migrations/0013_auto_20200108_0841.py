# Generated by Django 3.0 on 2020-01-08 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0012_auto_20200108_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='poll.Comment'),
        ),
    ]
