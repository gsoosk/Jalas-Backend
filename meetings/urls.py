from django.urls import path, include

from meetings.presentation import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from rest_framework.authtoken import views as auth_views


urlpatterns = [
    path('', views.create_meeting),
    path('all', views.get_meetings_list),
    path('available', views.get_available_rooms),
    path('cancel', views.cancel_reservation),
    # path('login', views.login),
    path('auth/', views.CustomAuthToken.as_view()),

    path('<int:meeting_id>', views.get_meeting_details, name='meeting_details'),
    # path('<int:pk>', views.MeetingInfoSerializer.as_view({'get': 'retrieve'}), name='meeting_details'),
]

