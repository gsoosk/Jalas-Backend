from poll.domain_logic.polls_service import get_all_polls_by_creator_name, get_poll_details_by_poll_id, add_new_votes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from reports.domain_logic.Reports import ReportsData
from rest_framework import viewsets, mixins
from poll.data import repo
from poll.presentation.serializers import PollSerializer
import poll.Exceptions as Exceptions


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
        ReportsData.get_instance().add_meeting_creation_time(request.session.session_key)
        return Response(output, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_404_NOT_FOUND)


class PollsViewSets(viewsets.GenericViewSet,
                    mixins.CreateModelMixin):
    queryset = repo.get_all_polls()
    serializer_class = PollSerializer


@api_view(['POST'])
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


