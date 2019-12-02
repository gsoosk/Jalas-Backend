from django.urls import path

from meetings.presentation import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.create_meeting),
    path('available', views.get_available_rooms),
    path('cancel', views.cancel_reservation),
    path('report', views.get_report)
]

urlpatterns = format_suffix_patterns(urlpatterns)
