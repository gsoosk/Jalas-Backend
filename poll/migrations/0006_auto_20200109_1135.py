# Generated by Django 3.0 on 2020-01-09 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0005_auto_20200109_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollchoiceitem',
            name='agrees',
            field=models.IntegerField(choices=[(1, 'AGREE'), (3, 'AGREE_IFNEEDED'), (2, 'DISAGREE')]),
        ),
    ]
