from django.urls import path
from rest_framework import routers, serializers, viewsets
from django.conf.urls import url
from poll.presentation import views


urlpatterns = [
    path('<int:poll_id>', views.get_poll_details, name='poll_details'),
    url(r'$', views.get_polls, name='all_polls')
]
