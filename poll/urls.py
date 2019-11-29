from django.urls import path

from poll.presentation import views

urlpatterns = [
    path('', views.get_polls, name='index'),
]