from poll.domain_logic.polls_service import get_all_polls_by_creator_name, get_poll_details_by_poll_id, add_new_votes, \
    add_new_comment_to_poll, get_comments, add_new_reply_to_comment, remove_comment_from_poll
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from report.domain_logic.Reports import ReportsData
from rest_framework import viewsets, mixins
from poll.data import repo
from poll.presentation.serializers import PollSerializer, CommentSerializer
import poll.Exceptions as Exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_polls(request):
    user_id = request.user.id
    try:
        output = get_all_polls_by_creator_name(user_id)
        return Response(output, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_poll_details(request, poll_id=0):
    try:
        output = get_poll_details_by_poll_id(poll_id)
        ReportsData.get_instance().add_meeting_creation_time(request.session.session_key)
        return Response(output, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_404_NOT_FOUND)


class CanChangePoll(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'update' or view.action == 'retrieve':
            instance = view.queryset.get(pk=view.kwargs['pk'])
            if not instance.creator.id == request.user.id:
                return False
        return True


class PollsViewSets(viewsets.GenericViewSet,
                    mixins.UpdateModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,):

    authentication_classes = [TokenAuthentication]
    permission_classes = [CanChangePoll, IsAuthenticated]

    queryset = repo.get_all_polls()
    serializer_class = PollSerializer


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vote_for_poll(request):
    if 'voterName' not in request.data.keys() or 'pollID' not in request.data.keys():
        return Response({"message": "Provided information is not enough"}, status=status.HTTP_400_BAD_REQUEST)
    voter = request.data['voterName']
    poll_id = request.data['pollID']
    votes = request.data['votes']

    try:
        add_new_votes(voter, poll_id, votes)
    except Exceptions.NotParticipant as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": Exceptions.PARTICIPANT_ERROR})
    except Exceptions.InvalidEmail as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": Exceptions.EMAIL_ERROR})
    except Exceptions.InvalidPoll as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": Exceptions.POLL_ERROR})
    except Exceptions.InvalidChosenTime as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": Exceptions.TIME_ERROR})
    except Exceptions.VotedBefore as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": Exceptions.VOTED_BEFORE_ERROR})
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Exception"})

    return Response({}, status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_comment(request):
    try:
        user_id = request.user.id
        poll_id = request.data['poll_id']
        text = request.data['text']
        add_new_comment_to_poll(user_id, poll_id, text)
        return Response({}, status=status.HTTP_200_OK)
    except Exceptions.InvalidPoll as e:
        return Response({"message": "You do not have access to this poll."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": "Provided information is not enough."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_reply_comment(request):
    try:
        user_id = request.user.id
        comment_id = request.data['comment_id']
        text = request.data['text']
        add_new_reply_to_comment(user_id, comment_id, text)
        return Response({}, status=status.HTTP_200_OK)
    except Exceptions.InvalidPoll as e:
        return Response({"message": "You do not have access to this poll."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": "Provided information is not enough."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_comments_of_poll(request, poll_id=-1):
    try:
        if poll_id == -1:
            raise Exceptions.InvalidPoll
        user_id = request.user.id
        comments = get_comments(poll_id, user_id)
        all_comments = []
        for comment in comments:
            serializer = CommentSerializer(comment)
            # add_replies
            all_comments.append(serializer.data)
        return Response(all_comments, status=status.HTTP_200_OK)
    except Exceptions.InvalidPoll as e:
        return Response({"message": "You do not have access to this poll."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"message": "Provided information is not enough."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_comment(request):
    user_id = request.user.id
    comment_id = request.data['comment_id']
    try:
        remove_comment_from_poll(user_id, comment_id)
        return Response({}, status=status.HTTP_200_OK)
    except Exceptions.InvalidComment as e:
        return Response({"message": "You do not have access to this comment."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": "Provided information is not enough."}, status=status.HTTP_400_BAD_REQUEST)