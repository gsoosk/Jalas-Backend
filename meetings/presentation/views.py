from django.shortcuts import render
from django.http import HttpResponse
from meetings.data.Meeting import Meeting
from meetings.data.Room import Room
from meetings.data.Participant import Participant
from meetings.domain_logic.meeting_service import create_new_meeting
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from meetings.presentation.serializers import MeetingSerializer, RoomSerializer, ParticipantSerializer
# Create your views here.


# def index(name):
#     return HttpResponse("Hello World")

@api_view(['POST'])
def create_meeting(request):
    serializer = MeetingSerializer(data=request.data)
    if serializer.is_valid():
        room = Room(serializer.data['room_id'])
        participants = []
        for participant in serializer.data['participants_id']:
            participants.append(participant)
        meeting = Meeting(serializer.data['title'], serializer.data['start_date_time'],
                          serializer.data['end_date_time'], room, participants)
        create_new_meeting(meeting)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

