# Generated by Django 3.0 on 2020-01-08 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0009_remove_comment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='poll.Comment'),
        ),
    ]