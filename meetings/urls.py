from django.urls import path, include

from meetings.presentation import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers



urlpatterns = [
    path('', views.create_meeting),
    path('available', views.get_available_rooms),
    path('cancel', views.cancel_reservation),
    path('report', views.get_report),

    path('<int:meeting_id>', views.get_meeting_details, name='meeting_details'),
    # path('<int:pk>', views.MeetingInfoSerializer.as_view({'get': 'retrieve'}), name='meeting_details'),
]

