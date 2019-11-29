# from poll.domain_logic.polls_service import get_all_polls_by_creator_name
# from django.http import HttpResponse
from poll.models import MeetingPoll, PollChoiceItem


def get_polls(creator_name):
    polls = []

    polls_models = MeetingPoll.objects.filter(creator__name=creator_name)
    for p in polls_models:
        polls.append(MeetingPoll(p.title))
    return polls


def get_choices(poll_title):
    choices = []

    choices_models = PollChoiceItem.objects.filter(poll__title=poll_title)
    for c in choices_models:
        start = c.chosen_time.start_date_time
        end = c.chosen_time.end_date_time

        found = False
        for prev_choice in choices:
            if prev_choice.hasSameTime(start, end):
                prev_choice.voters.append(c.voter.name)
                found = True
                break
        if not found:
            choices.append(PollChoiceItem([c.voter.name], start, end))
    return choices