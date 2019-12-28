from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from report.domain_logic.Reports import ReportsData


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_report(request):
    report = ReportsData.get_instance()
    average = 0
    if report.num_created_meetings > 0:
        average = report.sum_meeting_creation_time / report.num_created_meetings

    return Response({"Average Creation Time": str(average), "Number of reserved rooms":  str(report.num_reserved_rooms),
                     "Number of cancelled/modified meetings": str(report.num_cancelled_or_modified_meetings),
                     "Average response time": str(report.average_response_time) + " micro seconds"})

