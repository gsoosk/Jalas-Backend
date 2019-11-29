from django.db import models


class PollTime(models.Model):
    start_date_time = models.DateTimeField('Start time')
    end_date_time = models.DateTimeField('End time')


class MeetingPoll(models.Model):
    title = models.CharField(max_length=100)
    choices = models.ManyToManyField('PollTime')
    creator = models.ForeignKey('meetings.Participant', on_delete=models.CASCADE)


class PollChoiceItem(models.Model):
    voter = models.ForeignKey('meetings.Participant', on_delete=models.CASCADE)
    poll = models.ForeignKey('MeetingPoll', on_delete=models.CASCADE)
    chosen_time = models.ForeignKey('PollTime', on_delete=models.CASCADE)

