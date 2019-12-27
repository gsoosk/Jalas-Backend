from django.urls import path, include
from rest_framework import routers
from django.conf.urls import url
from poll.presentation import views

router = routers.DefaultRouter()
router.register(r'', views.PollsViewSets)

urlpatterns = [
    path('<int:poll_id>', views.get_poll_details, name='poll_details'),
    path('', views.get_polls, name='all_polls'),
    path('create/', include(router.urls)),
    path('vote', views.vote_for_poll),
    path('comment', views.add_comment),
]
