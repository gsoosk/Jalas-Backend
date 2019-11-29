from django.db import models


class Room(models.Model):
    roomName = models.CharField(max_length=100)
    capacity = models.IntegerField(default=0)
    location = models.CharField(max_length=200)
    hasVideoProjector = models.BooleanField(default=False)


class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()


class Meeting(models.Model):
    title = models.CharField(max_length=100)
    startDateTime = models.DateTimeField('Start time')
    endDateTime = models.DateTimeField('End time')
    room = models.ForeignKey('Room', null=True, on_delete=models.SET_NULL)
    participants = models.ManyToManyField('Participant')

