from collections import OrderedDict

from django.test import TestCase
from poll.models import MeetingPoll, PollTime
from meetings.models import Participant
from django.utils import timezone
from poll.presentation.serializers import PollSerializer
from rest_framework import serializers
from json import dumps
from rest_framework.renderers import JSONRenderer
# Create your tests here.


class CreatePollIntegrationsTests(TestCase):
    def setUp(self):
        self.start = timezone.now()
        self.end = timezone.now()
        self.creator = Participant.objects.create(email="p1@p.com")
        self.creator.save()
        self.start_str = serializers.DateTimeField().to_representation(self.start)
        self.end_str = serializers.DateTimeField().to_representation(self.end)
        self.create_data = {'title': 'fake', 'choices': [OrderedDict([('start_date_time', self.start_str), ('end_date_time', self.end_str)])], 'creator_id': 1, 'participants': [OrderedDict([('email', 'p2@p.com')])]}

    def testCreatePollRequest(self):
        response = self.client.post('/polls/create/', data=self.create_data, content_type='application/json')
        self.assertEqual(response.content, JSONRenderer().render(self.create_data))

    def tearDown(self):
        self.creator.delete()
