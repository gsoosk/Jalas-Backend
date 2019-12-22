from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class Room(models.Model):
    room_name = models.IntegerField()
    capacity = models.IntegerField(default=0)
    location = models.CharField(max_length=200, default="")
    has_video_projector = models.BooleanField(default=False)


class Participant(AbstractUser):
    # name = models.CharField(max_length=100) #name field was unnecessary
    # Removing Django User Unnecessary Fields :
    username = None
    first_name = None
    last_name = None
    # Change user name to email
    email = models.EmailField(_('email address'), unique=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'


class Meeting(models.Model):
    title = models.CharField(max_length=100)
    start_date_time = models.DateTimeField('Start time')
    end_date_time = models.DateTimeField('End time')
    room = models.ForeignKey('Room', null=True, on_delete=models.SET_NULL)
    participants = models.ManyToManyField('Participant')
    is_cancelled = models.BooleanField(default=False)
