# Generated by Django 2.2.7 on 2019-12-28 11:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0004_report_req_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='first_request_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='report',
            name='last_request_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]