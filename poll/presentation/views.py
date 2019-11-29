from django.shortcuts import render
from poll.domain_logic.polls_service import get_all_polls_by_creator_name
from django.http import HttpResponse


def get_polls(request):
    polls = get_all_polls_by_creator_name('Farzad')
    names = ','.join([p.title for p in polls])
    return HttpResponse(names)

# Create your views here.