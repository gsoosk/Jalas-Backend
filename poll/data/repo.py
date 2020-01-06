from poll.models import MeetingPoll, PollChoiceItem, PollTime, Comment, Reply
from poll.data.PollChoiceItem import PollChoiceItemRep
import poll.Exceptions as Exceptions
from meetings.models import Participant
from meetings.domain_logic.email_service import send_email
import _thread as thread
import datetime


def has_access_to_poll(user_id, poll):

    participants = poll.participants
    creator = poll.creator

    if user_id == creator.id:
        return True
    try:
        for participant in participants.iterator():
            if participant.id == user_id:
                return True
        return False
    except:
        return False


def get_polls(user_id):
    user_polls = []
    polls = MeetingPoll.objects.all()
    for poll in polls:
        if has_access_to_poll(user_id, poll):
            user_polls.append(poll)
    output = {'user_id': user_id, 'polls': [{'title': p.title, 'poll_id': p.id, 'creator_id': p.creator.id} for p in user_polls]}
    return output


def add_comment(user_id, poll_id, text):
    if not MeetingPoll.objects.filter(id=poll_id).exists():
        raise Exceptions.InvalidPoll
    poll = MeetingPoll.objects.filter(id=poll_id)[0]
    if not has_access_to_poll(user_id, poll):
        raise Exceptions.InvalidPoll
    user = Participant.objects.filter(id=user_id)[0]
    curr_time = datetime.datetime.now()
    comment = Comment(user=user, poll=poll, text=text, date_time=curr_time)
    comment.save()


def add_reply(user_id, comment_id, text):
    if not Comment.objects.filter(id=comment_id).exists():
        print('invalid comment')
        raise Exceptions.InvalidComment
    comment = Comment.objects.filter(id=comment_id)[0]

    if not has_access_to_poll(user_id, comment.poll):
        print('invalid poll')
        raise Exceptions.InvalidPoll
    user = Participant.objects.filter(id=user_id)[0]
    curr_time = datetime.datetime.now()
    reply = Reply(user=user, comment=comment, text=text, date_time=curr_time)
    reply.save()


def get_all_polls():
    polls = MeetingPoll.objects.all()
    return polls


def get_choices(poll_id, user_id):
    choices = []

    if not MeetingPoll.objects.filter(id=poll_id).exists():
        raise Exceptions.PollNotExists
    poll = MeetingPoll.objects.get(id=poll_id)
    if not (check_if_person_is_participant_of_poll_by_id(poll, user_id) or poll.creator == user_id):
        raise Exceptions.AccessDenied

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


def check_if_person_is_participant_of_poll_by_id(poll, user_id):
    participants = poll.participants.all()

    if participants.filter(id=user_id):
        return True
    return False


def check_if_person_has_voted_before(poll_id, participant_id):
    if PollChoiceItem.objects.filter(voter=participant_id, poll=poll_id):
        return True
    return False


def send_email_to_poll_creator(voter, poll):
    thread.start_new_thread(send_email, (f'New vote for {poll.title}',
                                         f'There is a vote for {poll.title} from {voter}',
                                         [poll.creator.email]))


def get_comments_of_poll(poll_id, user_id):
    if not MeetingPoll.objects.filter(id=poll_id).exists():
        raise Exceptions.InvalidPoll
    poll = MeetingPoll.objects.filter(id=poll_id)[0]
    if not has_access_to_poll(user_id, poll):
        raise Exceptions.InvalidPoll
    return Comment.objects.filter(poll=poll)


def get_replies_of_comment(comment_id, user_id):
    if not Comment.objects.filter(id=comment_id).exists():
        raise Exceptions.InvalidComment
    comment = Comment.objects.filter(id=comment_id)[0]
    return Reply.objects.filter(comment=comment)


def add_new_votes_to_poll(voter, poll_id, votes):
    if MeetingPoll.objects.get(id=poll_id):
        poll = MeetingPoll.objects.get(id=poll_id)
    else:
        raise Exceptions.InvalidPoll
    if poll.participants.filter(id=voter):
        voter_participant = poll.participants.filter(id=voter)[0]
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


def remove_poll_comment(user_id, comment_id):
    if Comment.objects.get(id=comment_id):
        comment = Comment.objects.get(id=comment_id)
        if not comment.user.id == user_id:
            raise Exception.AccessDenied
        else:
            comment.delete()
    else:
        raise Exceptions.InvalidComment
