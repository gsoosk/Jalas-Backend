from collections import OrderedDict

from django.test import TestCase
from poll.models import MeetingPoll, PollTime
from meetings.models import Participant
from django.utils import timezone
from poll.presentation.serializers import ParticipantModelSerializer, PollTimeSerializer,PollSerializer
from rest_framework import serializers
# Create your tests here.


class CreatePollTests(TestCase):
    def setUp(self):
        self.creator = Participant.objects.create(email="p1@p.com", password="s")
        self.poll = MeetingPoll.objects.create(title='fake', creator=self.creator)
        self.participant = Participant.objects.create(email="p2@p.com")
        self.poll.participants.add(self.participant)
        self.start = timezone.now()
        self.end = timezone.now()
        self.choice = PollTime.objects.create(start_date_time=self.start, end_date_time=self.end)
        self.poll.choices.add(self.choice)


    def testParticipantSerialization(self):
        serializer = ParticipantModelSerializer(self.participant)
        self.assertEqual(serializer.data, {'email': 'p2@p.com'})

    def testPollTimeSerialization(self):
        serializer = PollTimeSerializer(self.choice)
        start = serializers.DateTimeField().to_representation(self.start)
        end = serializers.DateTimeField().to_representation(self.end)
        self.assertEqual(serializer.data, {'start_date_time': start, 'end_date_time': end})

    def testPollSerialization(self):
        serializer = PollSerializer(self.poll)
        start = serializers.DateTimeField().to_representation(self.start)
        end = serializers.DateTimeField().to_representation(self.end)
        self.assertEqual(serializer.data, {'id':1, 'title': 'fake', 'choices': [OrderedDict([('start_date_time', start), ('end_date_time', end)])], 'creator_id': 1, 'participants': ['p2@p.com'], 'closed': False})

    def tearDown(self):
        self.poll.delete()
        self.choice.delete()
        self.participant.delete()
        self.creator.delete()
