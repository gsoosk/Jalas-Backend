from poll.domain_logic.polls_service import get_all_polls_by_user_id, get_poll_details_by_poll_id, add_new_votes, \
    add_new_comment_to_poll, get_comments, add_new_reply_to_comment, remove_comment_from_poll, close_poll_by_id
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
        output = get_all_polls_by_user_id(user_id)
        return Response(output, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_poll_details(request, poll_id=0):
    try:
        user_id = request.user.id
        output = get_poll_details_by_poll_id(poll_id, user_id)
        ReportsData.get_instance().add_meeting_creation_time(request.session.session_key)
        return Response(output, status=status.HTTP_200_OK)
    except Exceptions.AccessDenied as e:
        return Response({"message": "You do not have access to this poll"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exceptions.PollNotExists as e:
        return Response({"message": "This poll does not exist"}, status=status.HTTP_400_BAD_REQUEST)
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
    # if 'voterName' not in request.data.keys() or 'pollID' not in request.data.keys():
    if 'pollID' not in request.data.keys():
        return Response({"message": "Provided information is not enough"}, status=status.HTTP_400_BAD_REQUEST)

    voter = request.user.id
    poll_id = request.data['pollID']
    votes = request.data['votes']

    try:
        add_new_votes(voter, poll_id, votes)
    except Exceptions.NotParticipant:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": Exceptions.PARTICIPANT_ERROR})
    except Exceptions.InvalidEmail:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": Exceptions.EMAIL_ERROR})
    except Exceptions.InvalidPoll:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": Exceptions.POLL_ERROR})
    except Exceptions.InvalidChosenTime:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": Exceptions.TIME_ERROR})
    except Exceptions.VotedBefore:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": Exceptions.VOTED_BEFORE_ERROR})
    except Exceptions.PollClosed:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"message": "This poll is closed"})
    except Exception:
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
    except Exceptions.UserNotValid:
        return Response({"message": "The user you mentioned does not exist or does not have access to this poll."},
                        status=status.HTTP_404_NOT_FOUND)
    except Exceptions.InvalidPoll:
        return Response({"message": "You do not have access to this poll."}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
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
        return Response({"message": "You do not have access to this poll"}, status=status.HTTP_404_NOT_FOUND)
    except Exceptions.UserNotValid:
        return Response({"message": "The user you mentioned does not exist or does not have access to this poll."},
                        status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({"message": "Provided information is not enough"}, status=status.HTTP_400_BAD_REQUEST)


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
            comment_data = {'can_delete': repo.can_user_delete_comment(comment, request.user),
                            'can_edit': repo.can_edit_comment(comment, request.user)}
            comment_data.update(serializer.data)
            all_comments.append(comment_data)
        return Response(all_comments, status=status.HTTP_200_OK)
    except Exceptions.InvalidPoll as e:
        return Response({"message": "You do not have access to this poll"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"message": "Provided information is not enough"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_comment(request, id):
    comment = repo.get_comment(id)
    comment_data = {'can_delete': repo.can_user_delete_comment(comment, request.user),
                    'can_edit': repo.can_edit_comment(comment, request.user)}
    comment_data.update(CommentSerializer(comment).data)
    return Response(comment_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_comment(request):

    comment_id = request.data['comment_id']
    try:
        remove_comment_from_poll(request.user, comment_id)
        return Response({}, status=status.HTTP_200_OK)
    except Exceptions.InvalidComment as e:
        return Response({"message": "You do not have access to this comment"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": "Provided information is not enough"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def close_poll(request):
    user_id = request.user.id
    if 'poll_id' not in request.data.keys():
        return Response({"message": "Provided information is not enough"}, status=status.HTTP_400_BAD_REQUEST)
    poll_id = request.data['poll_id']
    try:
        close_poll_by_id(poll_id, user_id)
        return Response({}, status=status.HTTP_200_OK)
    except Exceptions.AccessDenied:
        return Response({"message": "You are not allowed to close this poll"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exceptions.InvalidPoll:
        return Response({"message": "This poll does not exist"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exceptions.AlreadyClosed:
        return Response({"message": "This poll is already closed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as e:
        return Response({"message": "An error has occurred"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_comment(request, comment_id):
    try:
        comment = repo.get_comment(comment_id)
    except:
        return Response({"message": "can not find comment"}, status=status.HTTP_404_NOT_FOUND)
    if not repo.can_edit_comment(comment, request.user):
        return Response({"message": "can not edit this comment"}, status=status.HTTP_403_FORBIDDEN)
    new_text = request.data['text']
    repo.update_comment(comment, new_text)
    return Response({}, status=status.HTTP_200_OK)
