from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver



class Room(models.Model):
    room_name = models.IntegerField()
    capacity = models.IntegerField(default=0)
    location = models.CharField(max_length=200, default="")
    has_video_projector = models.BooleanField(default=False)


class ParticipantManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


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

    objects = ParticipantManager()


class Notifications(models.Model):
    poll_creator_vote_notifications = models.BooleanField(default=True)
    poll_contribution_invitation = models.BooleanField(default=True)
    mention_notification = models.BooleanField(default=True)
    poll_close_notification = models.BooleanField(default=True)
    meeting_set_creator_notification = models.BooleanField(default=True)
    meeting_invitation = models.BooleanField(default=True)
    cancel_meeting_notification = models.BooleanField(default=True)
    owner = models.ForeignKey('Participant', on_delete=models.CASCADE, default=None, related_name='notification_owner')

@receiver(post_save, sender=Participant)
def add_notifications_to_new_user(sender, instance, **kwargs):
    user_notif = Notifications(owner=instance)
    user_notif.save()


class Meeting(models.Model):
    title = models.CharField(max_length=100)
    start_date_time = models.DateTimeField('Start time')
    end_date_time = models.DateTimeField('End time')
    room = models.ForeignKey('Room', null=True, on_delete=models.SET_NULL)
    participants = models.ManyToManyField('Participant', default=None, related_name='meeting_participants')
    creator = models.ForeignKey('Participant', on_delete=models.CASCADE, default=None, related_name='meeting_creator')
    is_cancelled = models.BooleanField(default=False)
