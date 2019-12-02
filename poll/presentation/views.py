from django.shortcuts import render
from poll.domain_logic.polls_service import get_all_polls_by_creator_name, get_poll_details
from django.http import HttpResponse
from poll.presentation.serializers import MeetingPollSerializer, ParticipantSerializer, PollChoiceItemSerializer
from django.http import HttpResponse, JsonResponse

from django.core import serializers
    # , PollsSerializer

def get_polls(request):
    user_id = request.GET['user']
    polls = get_all_polls_by_creator_name(user_id)
    serializer = MeetingPollSerializer(polls, many=True)
    pollss_json = serializers.serialize('json', polls)
    return JsonResponse(pollss_json, content_type='application/json', safe=False)


def get_poll_details(request, poll_id):
    choices = get_poll_details(poll_id)
    # names = ','.join([c.title for c in choices])
    return HttpResponse("")

