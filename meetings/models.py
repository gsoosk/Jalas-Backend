from django.db import models


class Room(models.Model):
    room_name = models.IntegerField()
    capacity = models.IntegerField(default=0)
    location = models.CharField(max_length=200, default="")
    has_video_projector = models.BooleanField(default=False)


class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()


class Meeting(models.Model):
    title = models.CharField(max_length=100)
    start_date_time = models.DateTimeField('Start time')
    end_date_time = models.DateTimeField('End time')
    room = models.ForeignKey('Room', null=True, on_delete=models.SET_NULL)
    participants = models.ManyToManyField('Participant')

