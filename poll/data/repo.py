# from poll.domain_logic.polls_service import get_all_polls_by_creator_name
# from django.http import HttpResponse
from meetings.models import Participant
from meetings.domain_logic import email_service
from poll.models import MeetingPoll, PollChoiceItem, PollTime
from poll.data.MeetingPolls import MeetingPollRep
from poll.data.PollChoiceItem import PollChoiceItemRep
import poll.Exceptions as Exceptions
from meetings.domain_logic.email_service import send_email
import _thread as thread

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
    poll_title = poll.title
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

        choices.append(PollChoiceItemRep(t.id, pos_voters, neg_voters, start, end))
    participant_ids = [participant.id for participant in participants]
    output = {'id': poll_id, 'title': poll_title, 'choices': [c.toJson() for c in choices], 'participants': participant_ids}

    return output


def get_new_poll(choices_data, creator, participants, title):
    poll = MeetingPoll.objects.create(creator=creator, title=title)

    for choice_data in choices_data:
        new_poll = PollTime.objects.create(**choice_data)
        poll.choices.add(new_poll)

    emails = []
    for new_participant in participants:
        emails.append(new_participant.email)
        poll.participants.add(new_participant)

    return poll, emails


def check_if_person_is_participant_of_poll(poll_id, participant_email):
    if MeetingPoll.objects.get(id=poll_id):
        poll = MeetingPoll.objects.get(id=poll_id)
        participants = poll.participants.all()

        if participants.filter(email=participant_email):
            return True
        return False
    else:
        raise Exceptions.InvalidPoll


def check_if_person_has_voted_before(poll_id, participant_id):
    if PollChoiceItem.objects.filter(voter=participant_id, poll=poll_id):
        print("^^^^^^^^^^^^^^^^voted before")
        return True
    print("^^^^^^^^^^^^^^^^has not voted before")
    return False


def send_email_to_poll_creator(voter, poll):
    thread.start_new_thread(send_email, (f'New vote for {poll.title}',
                                         f'There is a vote for {poll.title} from {voter}',
                                         [poll.creator.email]))


def add_new_votes_to_poll(voter, poll_id, votes):
    if MeetingPoll.objects.get(id=poll_id):
        poll = MeetingPoll.objects.get(id=poll_id)
    else:
        raise Exceptions.InvalidPoll
    if poll.participants.filter(email=voter):
        voter_participant = poll.participants.filter(email=voter)[0]
        if check_if_person_has_voted_before(poll_id, voter_participant.id):
            raise Exceptions.VotedBefore

        for chosen_time, agree in votes.items():
            if PollTime.objects.get(id=chosen_time):
                chosen_poll_time = PollTime.objects.get(id=chosen_time)
                choice_item = PollChoiceItem(voter=voter_participant, poll=poll, chosen_time=chosen_poll_time, agrees=agree)
                choice_item.save()
            else:
                raise Exceptions.InvalidChosenTime
        send_email_to_poll_creator(voter, poll)
    else:
        print("participant not found")
        raise Exceptions.NotParticipant
