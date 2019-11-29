from django.db import models


class PollTime(models.Model):
    startDateTime = models.DateTimeField('Start time')
    endDateTime = models.DateTimeField('End time')


class MeetingPoll(models.Model):
    title = models.CharField(max_length=100)
    choices = models.ManyToManyField('PollTime')


class PollChoiceItem(models.Model):
    voters = models.ForeignKey('meetings.Participant', on_delete=models.CASCADE)
    poll = models.ForeignKey('MeetingPoll', on_delete=models.CASCADE)
    chosenTime = models.ForeignKey('PollTime', on_delete=models.CASCADE)

