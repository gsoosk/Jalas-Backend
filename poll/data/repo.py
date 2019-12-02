# from poll.domain_logic.polls_service import get_all_polls_by_creator_name
# from django.http import HttpResponse

from poll.models import MeetingPoll, PollChoiceItem, PollTime
from poll.data.MeetingPolls import MeetingPollRep
from poll.data.PollChoiceItem import PollChoiceItemRep


def get_polls(creator_id):
    polls= MeetingPoll.objects.filter(creator__id=creator_id)
    output = {'creator_id': creator_id, 'polls': [{'title' : p.title, 'id': p.id} for p in polls]}
    return output


def get_choices(poll_id):
    choices = []

    poll = MeetingPoll.objects.get(id=poll_id)
    poll_times = poll.choices.all()

    choices_models = PollChoiceItem.objects.filter(poll__id=poll_id)

    for t in poll_times:
        votes = PollChoiceItem.objects.filter(poll=poll_id, chosen_time=t.id)

        start = t.start_date_time
        end = t.end_date_time

        pos_voters=[]
        neg_voters=[]
        for v in votes:
            if v.agrees:
                pos_voters.append(v.voter.id)
            else:
                neg_voters.append(v.voter.id)

        choices.append(PollChoiceItemRep(pos_voters, neg_voters, start, end))

        #
        # found = False
        # for prev_choice in choices:
        #     if prev_choice.hasSameTime(start, end):
        #         if c.agrees:
        #             prev_choice.positive_voters.append(c.voter.id)
        #         else:
        #             prev_choice.negative_voters.append(c.voter.id)
        #         found = True
        #         break
        # if not found:
        #     pos_voters = []
        #     neg_voters = []
        #     if c.agrees:
        #         pos_voters.append(c.voter.id)
        #     else:
        #         neg_voters.append(c.voter.id)
        #     choices.append(PollChoiceItemRep(pos_voters, neg_voters, start, end))
    # poll_times_out = [{'start_time': str(t.start_date_time), 'end_time': str(t.end_date_time)} for t in poll_times]

    output = {'id': poll_id, 'choices': [c.toJson() for c in choices]}

    return output
