from poll.domain_logic.polls_service import get_all_polls_by_creator_name, get_poll_details_by_poll_id
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from reports.domain_logic.Reports import ReportsData
from rest_framework import viewsets, mixins
from poll.data import repo
from poll.presentation.serializers import  PollSerializer

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
