from django.contrib.auth import authenticate

from meetings.data.Meeting import Meeting
from meetings.data.Room import Room
from meetings.domain_logic.meeting_service import create_new_meeting, cancel_room_reservation, \
    get_meeting_details_by_id, get_all_meetings_by_user_id, get_notifications_by_user, update_notifications
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from meetings.presentation.serializers import MeetingSerializer, MeetingInfoSerializer, SignupSerializer, NotificationSerializer
from meetings import Exceptions
from meetings.domain_logic.meeting_service import get_available_rooms_service
from report.domain_logic.Reports import ReportsData
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from meetings.models import Participant


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_meeting(request):
    user_id = request.user.id
    serializer = MeetingSerializer(data=request.data)
    if serializer.is_valid():
        room = Room(serializer.data['room_id'])
        participants = []
        for participant in serializer.data['participants_id']:
            participants.append(participant)
        meeting = Meeting(serializer.data['title'], serializer.data['start_date_time'],
                          serializer.data['end_date_time'], room, participants, user_id)
        try:
            meeting_id, reserved = create_new_meeting(meeting, str(request.get_host()).split(':')[0]
                                                      , str(3000))
            ReportsData.get_instance().finalize_meeting_time(request.session.session_key)
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
def signup(request):
    try:
        if request.data['is_staff'] == 'true' or request.data['is_staff']:
            Participant.objects.create_superuser(request.data['username'], request.data['password'])
        else:
            Participant.objects.create_user(request.data['username'], request.data['password'])
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message':str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cancel_reservation(request):
    user_id = request.user.id
    if 'meeting_id' not in request.data.keys():
        return Response({"message": "No id in request"}, status=status.HTTP_400_BAD_REQUEST)
    data = request.data
    try:
        if 'after_creation' not in request.data.keys() or not data['after_creation']:
            if not ReportsData.get_instance().reserving:
                return Response({"message": "Already Reserved"}, status=status.HTTP_408_REQUEST_TIMEOUT)
        cancel_room_reservation(data['meeting_id'], user_id)
        ReportsData.get_instance().inc_cancelled(request.session.session_key)
        return Response(status=status.HTTP_200_OK)
    except Exceptions.UnauthorizedUser:
        return Response({"message:": "You are not allowed to cancel this meeting"}, status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exceptions.MeetingNotFound:
        return Response({"message:": "could not cancel"}, status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_meeting_details(request, meeting_id):
    try:
        user_id = request.user.id
        meeting = get_meeting_details_by_id(meeting_id, user_id)
        serializer = MeetingInfoSerializer(meeting)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exceptions.UnauthorizedUser as e:
        return Response({"message": "You do not have access to this meeting"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exceptions.MeetingNotExists as e:
        return Response({"message": "This meeting does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(e, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_meetings_list(request):
    try:
        user_id = request.user.id
        meetings = get_all_meetings_by_user_id(user_id)
        return Response(meetings, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_404_NOT_FOUND)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'is_admin': user.is_staff,
        })

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_norifications_info(request):
    try:
        user_id = request.user.id
        notifications = get_notifications_by_user(user_id)
        serializer = NotificationSerializer(notifications)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exceptions.InvalidParticipantInfo:
        return  Response({"message": "This user does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(e, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_norifications_info(request):
    try:
        user_id = request.user.id
        notifications = get_notifications_by_user(user_id)
        update_notifications(notifications, request)
        return Response(status=status.HTTP_200_OK)
    except Exceptions.InvalidParticipantInfo:
        return  Response({"message": "This user does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(e, status=status.HTTP_404_NOT_FOUND)
