from poll.models import MeetingPoll, PollChoiceItem, PollTime, Comment
from poll.data.PollChoiceItem import PollChoiceItemRep
import poll.Exceptions as Exceptions
from meetings.models import Participant, Notifications
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
    output = {'user_id': user_id, 'polls': [{'title': p.title, 'poll_id': p.id, 'deadline': p.deadline, 'creator_id': p.creator.id, 'closed': p.closed} for p in user_polls]}
    return output


def add_comment(user_id, poll_id, text):
    if not MeetingPoll.objects.filter(id=poll_id).exists():
        raise Exceptions.InvalidPoll
    poll = MeetingPoll.objects.filter(id=poll_id)[0]
    if not has_access_to_poll(user_id, poll):
        raise Exceptions.InvalidPoll
    user = Participant.objects.filter(id=user_id)[0]
    curr_time = datetime.datetime.now()
    comment = Comment(user=user, text=text, date_time=curr_time)
    comment.save()
    poll.comments.add(comment)


def get_poll_of_comment(comment):
    while comment.parent is not None:
        comment = comment.parent
    poll = MeetingPoll.objects.get(comments=comment)
    return poll


def add_reply(user_id, comment_id, text):
    if not Comment.objects.filter(id=comment_id).exists():
        print('invalid comment')
        raise Exceptions.InvalidComment
    comment = Comment.objects.filter(id=comment_id)[0]

    if not has_access_to_poll(user_id, get_poll_of_comment(comment)):
        print('invalid poll')
        raise Exceptions.InvalidPoll
    user = Participant.objects.get(id=user_id)
    curr_time = datetime.datetime.now()
    reply = Comment(user=user, text=text, date_time=curr_time, parent=comment)
    reply.save()


def get_all_polls():
    polls = MeetingPoll.objects.all()
    return polls


def get_choices(poll_id, user_id):
    choices = []

    if not MeetingPoll.objects.filter(id=poll_id).exists():
        raise Exceptions.PollNotExists
    poll = MeetingPoll.objects.get(id=poll_id)
    if not (check_if_person_is_participant_of_poll_by_id(poll_id, user_id) or poll.creator_id == user_id):
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
        ifneeded_voters=[]
        for v in votes:
            if v.agrees == 1:
                pos_voters.append(v.voter.id)
            elif v.agrees == 2:
                neg_voters.append(v.voter.id)
            elif v.agrees == 3:
               ifneeded_voters.append(v.voter.id)

        choices.append(PollChoiceItemRep(t.id, pos_voters, neg_voters, ifneeded_voters, start, end))
    participant_ids = [participant.id for participant in participants]
    output = {'id': poll_id, 'title': poll_title, 'deadline': poll.deadline, 'closed': poll.closed, 'choices': [c.toJson() for c in choices], 'participants': participant_ids}

    return output


def get_new_poll(choices_data, creator, participants, title, deadline, hasDeadline):
    poll = MeetingPoll.objects.create(creator=creator, title=title, closed=False, deadline=deadline,
                                      hasDeadline=hasDeadline)

    for choice_data in choices_data:
        new_poll = PollTime.objects.create(**choice_data)
        poll.choices.add(new_poll)

    emails = []
    for new_participant in participants:
        emails.append(new_participant.email)
        poll.participants.add(new_participant)

    poll.participants.add(creator)

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


def check_if_person_is_participant_of_poll_by_id(poll_id, user_id):
    if MeetingPoll.objects.get(id=poll_id):
        poll = MeetingPoll.objects.get(id=poll_id)
    else:
        raise Exceptions.InvalidPoll
    participants = poll.participants
    if participants.filter(id=user_id) or poll.creator.id == user_id:
        return True
    return False


def check_if_person_has_voted_before(poll_id, participant_id):
    if PollChoiceItem.objects.filter(voter=participant_id, poll=poll_id):
        return True
    return False

def delete_prev_user_votes(poll_id, participant_id):
    PollChoiceItem.objects.filter(voter=participant_id, poll=poll_id).delete()


def send_email_to_poll_creator(voter, poll, updated):
    notif = Notifications.objects.filter(owner=poll.creator.email)[0]
    if not notif.poll_creator_vote_notifications:
        return
    if updated:
        thread.start_new_thread(send_email, (f'Update vote for {poll.title}',
                                             f'The vote for {poll.title} from {voter} has been updated',
                                             [poll.creator.email]))
    else:
        thread.start_new_thread(send_email, (f'New vote for {poll.title}',
                                         f'There is a vote for {poll.title} from {voter}',
                                         [poll.creator.email]))


def get_comments_of_poll(poll_id, user_id):
    if not MeetingPoll.objects.filter(id=poll_id).exists():
        raise Exceptions.InvalidPoll
    poll = MeetingPoll.objects.filter(id=poll_id)[0]
    if not has_access_to_poll(user_id, poll):
        raise Exceptions.InvalidPoll
    return poll.comments.all()


def get_replies_of_comment(comment_id, user_id):
    if not Comment.objects.filter(id=comment_id).exists():
        raise Exceptions.InvalidComment
    comment = Comment.objects.filter(id=comment_id)[0]
    return Reply.objects.filter(comment=comment)


def add_new_votes_to_poll(voter, poll_id, votes):
    updated = False
    if MeetingPoll.objects.get(id=poll_id):
        poll = MeetingPoll.objects.get(id=poll_id)
    else:
        raise Exceptions.InvalidPoll
    if poll.closed:
        raise Exceptions.PollClosed
    if poll.participants.filter(id=voter):
        voter_participant = poll.participants.filter(id=voter)[0]
        if check_if_person_has_voted_before(poll_id, voter_participant.id):
            updated = True
            delete_prev_user_votes(poll_id, voter_participant.id)

        for chosen_time, agree in votes.items():
            if PollTime.objects.get(id=chosen_time):
                if agree == "agree":
                    agree_state = 1
                elif agree == "disagree":
                    agree_state = 2
                elif agree == "agree_ifneeded":
                    agree_state = 3

                chosen_poll_time = PollTime.objects.get(id=chosen_time)
                choice_item = PollChoiceItem(voter=voter_participant, poll=poll, chosen_time=chosen_poll_time, agrees=agree_state)
                choice_item.save()
            else:
                raise Exceptions.InvalidChosenTime
        send_email_to_poll_creator(voter, poll, updated)
    else:
        print("participant not found")
        raise Exceptions.NotParticipant
    return updated

def remove_poll_comment(user, comment_id):
    if Comment.objects.get(id=comment_id):
        comment = Comment.objects.get(id=comment_id)
        if not can_user_delete_comment(comment, user):
            raise Exception
        else:
            comment.delete()
    else:
        raise Exceptions.InvalidComment


def find_id_by_email(email):
    if Participant.objects.filter(email=email).exists():
        person = Participant.objects.get(email=email)
        return person.id
    else:
        raise Exceptions.UserNotValid


def create_choice_time(choice_data):
    return PollTime.objects.create(**choice_data)


def edit_title(instance, attr, value):
    setattr(instance, attr, value)
    instance.save()


def close_poll(poll_id, user_id):
    if not MeetingPoll.objects.filter(id=poll_id).exists():
        raise Exceptions.InvalidPoll
    poll = MeetingPoll.objects.filter(id=poll_id)[0]
    creator = poll.creator

    if not user_id == creator.id:
        raise Exceptions.AccessDenied
    if poll.closed:
        raise Exceptions.AlreadyClosed

    poll.closed = True
    poll.save()


def get_participants_emails(poll_id):
    if not MeetingPoll.objects.filter(id=poll_id).exists():
        raise Exceptions.InvalidPoll
    poll = MeetingPoll.objects.filter(id=poll_id)[0]
    participants = poll.participants
    emails = []
    for participant in participants.iterator():
        emails.append(participant.email)
    return emails


def remove_old_participants(instance):
    old_participant_emails = []
    for participant in instance.participants.iterator():
        old_participant_emails.append(participant.email)
        instance.participants.remove(participant)
    instance.save()
    return old_participant_emails


def add_new_participants(instance, participants_value, user):
    new_participant_emails = []
    for new_participant in participants_value:
        new_participant_emails.append(new_participant.email)
        instance.participants.add(new_participant)
    instance.participants.add(user)
    if user.email not in new_participant_emails :
        new_participant_emails.append(user.email)
        instance.save()
    return new_participant_emails


def is_choice_in_values(choice, choices_value):
    for choice_value in choices_value:
        if choice_value['start_date_time'] == choice.start_date_time and \
                choice_value['end_date_time'] == choice.end_date_time:
            return True
    return False


def remove_not_included_choices(instance, choices_value):
    for choice in instance.choices.iterator():
        if not is_choice_in_values(choice, choices_value):
            instance.remove(choice)
            choice.delete()
    instance.save()


def is_choice_value_in_choices(choice_value, choices):
    for choice in choices.iterator():
        if choice_value['start_date_time'] == choice.start_date_time and \
                choice_value['end_date_time'] == choice.end_date_time:
            return True
    return False


def add_new_choices(instance, choices_value):
    for choice_value in choices_value:
        if not is_choice_value_in_choices(choice_value, instance.choices):
            new_choice = create_choice_time(choice_value)
            instance.choices.add(new_choice)
    instance.save()


def get_comment(comment_id):
    return Comment.objects.get(id=comment_id)


def can_user_delete_comment(comment, user):
    if user == comment.user:
        return True
    while comment.parent is not None:
        comment = comment.parent
    try:
        poll = MeetingPoll.objects.get(comments=comment)
        if poll.creator == user:
            return True
    except:
        return False
    return False


def can_edit_comment(comment, user):
    if comment.user == user:
        return True
    return False


def update_comment(comment, new_text):
    comment.text = new_text
    comment.date_time = datetime.datetime.now()
    comment.save()
