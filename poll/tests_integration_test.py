from collections import OrderedDict

from django.test import TestCase
from poll.models import MeetingPoll, PollTime
from meetings.models import Participant
from django.utils import timezone
from poll.presentation.serializers import PollSerializer
from rest_framework import serializers
from json import dumps
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
import json
from django.contrib.auth import authenticate
# Create your tests here.


class CreatePollIntegrationsTests(TestCase):
    def setUp(self):
        self.start = timezone.now()
        self.end = timezone.now()
        self.creator = Participant.objects.create_user(email="p1@p.com", password="salam")
        dummy = Participant.objects.create(email="p2@p.com", password="salam")
        dummy.save()
        self.creator.save()
        login = self.client.post('/meetings/auth/', data={'username':'p1@p.com', 'password':'salam'})
        content = json.loads(login.content.decode("utf-8"))
        token = content['token']
        self.headers = {'Authorization': 'Token ' + token}
        self.start_str = serializers.DateTimeField().to_representation(self.start)
        self.end_str = serializers.DateTimeField().to_representation(self.end)
        self.create_data = {'title': 'fake', 'choices': [OrderedDict([('start_date_time', self.start_str), ('end_date_time', self.end_str)])], 'participants': ['p2@p.com']}

    def testCreatePollRequest(self):
        response = self.client.post('/polls/create/', data=self.create_data, content_type='application/json', **self.headers)
        # self.assertEqual(response.content, JSONRenderer().render(self.create_data))

    def tearDown(self):
        self.creator.delete()
