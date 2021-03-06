# Generated by Django 3.0 on 2020-01-09 07:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import meetings.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', meetings.models.ParticipantManager()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.IntegerField()),
                ('capacity', models.IntegerField(default=0)),
                ('location', models.CharField(default='', max_length=200)),
                ('has_video_projector', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('start_date_time', models.DateTimeField(verbose_name='Start time')),
                ('end_date_time', models.DateTimeField(verbose_name='End time')),
                ('is_cancelled', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='meeting_creator', to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(default=None, related_name='meeting_participants', to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='meetings.Room')),
            ],
        ),
    ]
