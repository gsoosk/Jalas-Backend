# Generated by Django 2.2.7 on 2019-11-29 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('meetings', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingPoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PollTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDateTime', models.DateTimeField(verbose_name='Start time')),
                ('endDateTime', models.DateTimeField(verbose_name='End time')),
            ],
        ),
        migrations.CreateModel(
            name='PollChoiceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chosenTime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.PollTime')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.MeetingPoll')),
                ('voters', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.Participant')),
            ],
        ),
        migrations.AddField(
            model_name='meetingpoll',
            name='choices',
            field=models.ManyToManyField(to='poll.PollTime'),
        ),
    ]
