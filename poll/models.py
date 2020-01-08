from django.db import models
from django.utils.timezone import now


class PollTime(models.Model):
    start_date_time = models.DateTimeField('Start time', default=now)
    end_date_time = models.DateTimeField('End time', default=now)


class MeetingPoll(models.Model):
    title = models.CharField(max_length=100)
    choices = models.ManyToManyField('PollTime', default=None)
    creator = models.ForeignKey('meetings.Participant', on_delete=models.CASCADE, default=None, related_name='creator')
    participants = models.ManyToManyField('meetings.Participant', default=None, related_name='participants')
    comments = models.ManyToManyField('Comment', default=None, related_name='comments')


class PollChoiceItem(models.Model):
    voter = models.ForeignKey('meetings.Participant', on_delete=models.CASCADE, default=None)
    poll = models.ForeignKey('MeetingPoll', on_delete=models.CASCADE, default=None)
    chosen_time = models.ForeignKey('PollTime', on_delete=models.CASCADE, default=None)
    agrees = models.BooleanField(default=False)


class Comment(models.Model):
    user = models.ForeignKey('meetings.Participant', on_delete=models.CASCADE, default=None)
    text = models.TextField(default="")
    date_time = models.DateTimeField('Created time', default=now)
    parent = models.ForeignKey('self', default=None, on_delete=models.CASCADE, null=True, related_name='replies')
