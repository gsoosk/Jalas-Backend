# from poll.domain_logic.polls_service import get_all_polls_by_creator_name
# from django.http import HttpResponse

from poll.models import MeetingPoll, PollChoiceItem
from poll.data.MeetingPolls import MeetingPollRep
from poll.data.PollChoiceItem import PollChoiceItemRep


def get_polls(creator_id):

    polls= MeetingPoll.objects.filter(creator__id=creator_id)
    output = {'creator_id': creator_id, 'polls': [p.title for p in polls]}
    return output


def get_choices(poll_id):
    choices = []

    choices_models = PollChoiceItem.objects.filter(poll__id=poll_id)
    for c in choices_models:
        start = c.chosen_time.start_date_time
        end = c.chosen_time.end_date_time

        found = False
        for prev_choice in choices:
            if prev_choice.hasSameTime(start, end):
                if c.agrees:
                    prev_choice.positive_voters.append(c.voter.id)
                else:
                    prev_choice.negative_voters.append(c.voter.id)
                found = True
                break
        if not found:
            pos_voters = []
            neg_voters = []
            if c.agrees:
                pos_voters.append(c.voter.id)
            else:
                neg_voters.append(c.voter.id)
            choices.append(PollChoiceItemRep(pos_voters, neg_voters, start, end))

    output = {'id': poll_id, 'choices': [c.toJson() for c in choices]}

    return output
