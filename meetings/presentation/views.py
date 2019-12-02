from meetings.data.Meeting import Meeting
from meetings.data.Room import Room
from meetings.domain_logic.meeting_service import create_new_meeting, cancel_room_reservation
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from meetings.presentation.serializers import MeetingSerializer
from meetings import Exceptions
from meetings.domain_logic.meeting_service import get_available_rooms_service
from meetings.domain_logic.meeting_service import reserving


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
            meeting_id, reserved = create_new_meeting(meeting)
        except Exceptions.InvalidParticipantInfo:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED,
                            data={"message": "At least one participant is not valid."})
        except Exceptions.RoomCanNotBeReserved as e :
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={"message": "Room Reserved Already"})
        except Exceptions.RoomTimeInvalid as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Time Is Invalid"})
        except Exceptions.RoomIsNotAvailable as e :
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={"message": "Room Is Not Available"})

        return Response({'id':meeting_id, 'reserved':reserved}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_available_rooms(request):
    if 'start_date_time' not in request.data.keys() or 'end_date_time' not in request.data.keys():
        return Response({"message": "bad time"}, status=status.HTTP_400_BAD_REQUEST)
    data = request.data
    try:
        rooms = get_available_rooms_service(data['start_date_time']+'Z', data['end_date_time']+'Z')
    except Exceptions.RoomTimeInvalid as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Time Is Invalid"})
    except:
        return Response(status=status.HTTP_423_LOCKED, data={"message":"Server Is Down"})

    return Response({"rooms": list(rooms.keys())}, status.HTTP_200_OK)


@api_view(['POST'])
def cancel_reservation(request):
    if 'meeting_id' not in request.data.keys():
        return Response({"message": "No id in request"}, status=status.HTTP_400_BAD_REQUEST)
    data = request.data
    try:
        if not reserving:
            return Response({"message": "Already Reserved"}, status=status.HTTP_408_REQUEST_TIMEOUT)
        cancel_room_reservation(data['meeting_id'])
        return Response(status=status.HTTP_200_OK)
    except Exceptions.MeetingNotFound:
        return Response({"message:": "could not cancel"}, status.HTTP_405_METHOD_NOT_ALLOWED)

