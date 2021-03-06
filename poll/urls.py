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
    path('comment/<int:id>/', views.get_comment),
    path('comment', views.add_comment),
    path('update_comment/<int:comment_id>/', views.update_comment),
    path('reply_comment', views.add_reply_comment),
    path('comments/<int:poll_id>/', views.get_comments_of_poll),
    path('remove_comment/', views.remove_comment),
    path('close', views.close_poll)
]
