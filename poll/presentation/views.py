from django.shortcuts import render
from poll.domain_logic.polls_service import get_all_polls_by_creator_name, get_poll_details_by_poll_id
from django.http import HttpResponse
from poll.presentation.serializers import MeetingPollSerializer, ParticipantSerializer, PollChoiceItemSerializer
from django.http import HttpResponse, JsonResponse
import json
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from reports.domain_logic.Reports import ReportsData


@api_view(['GET'])
def get_polls(request):
    user_id = request.GET['user']
    try:
        output = get_all_polls_by_creator_name(user_id)
        return Response(output, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_poll_details(request, poll_id=0):
    try:
        output = get_poll_details_by_poll_id(poll_id)
        ReportsData.add_meeting_creation_time(request.session.session_key)
        return Response(output, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_404_NOT_FOUND)
