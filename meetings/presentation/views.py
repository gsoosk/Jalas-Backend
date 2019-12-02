from meetings.data.Meeting import Meeting
from meetings.data.Room import Room
from meetings.domain_logic.meeting_service import create_new_meeting
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from meetings.presentation.serializers import MeetingSerializer
from meetings import Exceptions
from meetings.domain_logic.meeting_service import get_available_rooms_service
import json


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
        try:
            create_new_meeting(meeting)

        except Exceptions.RoomCanNotReserved as e :
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={"message" : "Room Reserved Already"})
        except Exceptions.RoomTimeInvalid as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message" : "Time Is Invalid"})
        except Exceptions.RoomIsNotAvailable as e :
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={"message" : "Room Is Not Available"})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_available_rooms(request):
    if 'start_date_time' not in request.data.keys() or 'end_date_time' not in request.data.keys() :
        return Response({"message":"bad time"}, status=status.HTTP_400_BAD_REQUEST)
    data = request.data
    rooms = {}
    try:
        rooms = get_available_rooms_service(data['start_date_time']+'Z', data['end_date_time']+'Z')
    except Exceptions.RoomTimeInvalid as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Time Is Invalid"})
    return Response({"rooms":list(rooms.keys())}, status.HTTP_200_OK)
