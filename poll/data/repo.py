# from poll.domain_logic.polls_service import get_all_polls_by_creator_name
# from django.http import HttpResponse
from meetings.models import Participant
from meetings.domain_logic import email_service
from poll.models import MeetingPoll, PollChoiceItem, PollTime
from poll.data.MeetingPolls import MeetingPollRep
from poll.data.PollChoiceItem import PollChoiceItemRep


def get_polls(creator_id):
    polls = MeetingPoll.objects.filter(creator__id=creator_id)
    output = {'creator_id': creator_id, 'polls': [{'title': p.title, 'id': p.id} for p in polls]}
    return output


def get_all_polls():
    polls = MeetingPoll.objects.all()
    return polls


def get_choices(poll_id):
    choices = []

    poll = MeetingPoll.objects.get(id=poll_id)
    poll_times = poll.choices.all()
    participants = poll.participants.all()

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

    participant_ids = [participant.id for participant in participants]
    output = {'id': poll_id, 'choices': [c.toJson() for c in choices], 'participants': participant_ids}

    return output


def get_new_poll(choices_data, creator_data, participants_data, title):
    creator = Participant.objects.get(pk=creator_data['id'])
    poll = MeetingPoll.objects.create(creator=creator, title=title)

    for choice_data in choices_data:
        new_poll = PollTime.objects.create(**choice_data)
        poll.choices.add(new_poll)

    emails = []
    for participant_data in participants_data:
        new_participant = Participant.objects.create(**participant_data)
        emails.append(new_participant.email)
        poll.participants.add(new_participant)

    return poll, emails
