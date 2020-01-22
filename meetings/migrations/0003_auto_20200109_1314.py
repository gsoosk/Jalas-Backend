# Generated by Django 3.0 on 2020-01-09 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0002_notifications'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notifications',
            old_name='email_to_poll_creator',
            new_name='meeting_set_creator_notification',
        ),
        migrations.RenameField(
            model_name='notifications',
            old_name='meeting_creator_notification',
            new_name='poll_contribution_invitation',
        ),
        migrations.RenameField(
            model_name='notifications',
            old_name='poll_email_to_participants',
            new_name='poll_creator_vote_notifications',
        ),
    ]