# Generated by Django 3.0 on 2020-01-09 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollchoiceitem',
            name='agrees',
            field=models.IntegerField(choices=[(3, 'AGREE_IFNEEDED'), (1, 'AGREE'), (2, 'DISAGREE')]),
        ),
    ]