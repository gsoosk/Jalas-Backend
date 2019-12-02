from django.shortcuts import render
from poll.domain_logic.polls_service import get_all_polls_by_creator_name, get_poll_details_by_poll_id
from django.http import HttpResponse
from poll.presentation.serializers import MeetingPollSerializer, ParticipantSerializer, PollChoiceItemSerializer
from django.http import HttpResponse, JsonResponse
import json


from django.core import serializers
    # , PollsSerializer

def get_polls(request):
    user_id = request.GET['user']
    output = get_all_polls_by_creator_name(user_id)
    # serializer = MeetingPollSerializer(polls, many=True)
    # pollss_json = serializers.serialize('json', polls)
    # return HttpResponse(json.dumps(polls.__dict__), content_type="application/json")\
    # print("******")
    # print([poll.get_title() for poll in polls])
    # print(json.dumps([dict(poll) for poll in polls]))
    # return JsonResponse(json.dumps([poll.__dict__ for poll in polls]), content_type='application/json', safe=False)
    return JsonResponse(json.dumps(output), safe=False)


def get_poll_details(request, poll_id=0):
    output = get_poll_details_by_poll_id(poll_id)
    return JsonResponse(json.dumps(output), safe=False)

