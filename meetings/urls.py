from django.urls import path

from meetings.presentation import views

urlpatterns = [
    path('', views.index, name='index'),
]