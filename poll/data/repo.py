# from poll.domain_logic.polls_service import get_all_polls_by_creator_name
# from django.http import HttpResponse
from meetings.models import Participant
from meetings.domain_logic import email_service
from poll.models import MeetingPoll, PollChoiceItem, PollTime
from poll.data.MeetingPolls import MeetingPollRep
from poll.data.PollChoiceItem import PollChoiceItemRep
import poll.Exceptions as Exceptions


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


def check_if_person_is_participant_of_poll(poll_id, participant_id):
    if MeetingPoll.objects.get(id=poll_id):
        poll = MeetingPoll.objects.get(id=poll_id)
        participants = poll.participants.all()

        if participants.filter(pk=participant_id):
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


def add_new_votes_to_poll(voter, poll_id, votes):
    if Participant.objects.filter(email=voter):
        voter_participant = Participant.objects.filter(email=voter)[0]
        if not check_if_person_is_participant_of_poll(poll_id, voter_participant.id):
            print("not a participant of this poll")
            raise Exceptions.NotParticipant
        if check_if_person_has_voted_before(poll_id, voter_participant.id):
            raise Exceptions.VotedBefore

        poll = MeetingPoll.objects.get(id=poll_id)
        for chosen_time, agree in votes.items():
            if PollChoiceItem.objects.get(id=chosen_time):
                chosen_poll_time = PollTime.objects.get(id=chosen_time)
                choice_item = PollChoiceItem(voter=voter_participant, poll=poll, chosen_time=chosen_poll_time, agrees=agree)
                choice_item.save()
            else:
                raise Exceptions.InvalidChosenTime


    else:
        print("participant not found")
        raise Exceptions.InvalidEmail
