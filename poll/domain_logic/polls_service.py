from poll import Exceptions
from poll.data.repo import get_polls, get_choices, add_new_votes_to_poll, add_comment, get_comments_of_poll, add_reply \
    , remove_poll_comment, check_if_person_is_participant_of_poll_by_id, find_id_by_email, create_choice_time
from meetings.domain_logic.email_service import send_email
import _thread as thread
import re


def get_all_polls_by_user_id(user_id):
    try:
        return get_polls(user_id)
    except Exception as e:
        raise Exception()


def get_poll_details_by_poll_id(poll_id, user_id):
    try:
        return get_choices(poll_id, user_id)
    except Exception as e:
        raise e


def send_poll_email_to_participants(emails, title, poll_id):
    thread.start_new_thread(send_email, (
        "Poll Contribution Invitation", "You have been invited to a poll called " + title + " in Jalas"
        + "\nYou can view this poll using the URL below:\n"
        + "http://" + "localhost" + ":" + "3000" + "/polls/" + str(poll_id), emails))


def send_mention_notification(email, poll_id):
    send_email("Mention Notification", "You are mentioned in a comment:\n"
               "\nYou can view this comment in the following URL:\n"
               + "http://localhost:3000/comments/" + poll_id, [email])


def add_new_votes(voter, poll_id, votes):
    try:
        add_new_votes_to_poll(voter, poll_id, votes)
    except Exception as e:
        raise e


def extract_mention(text):
    results = re.findall(r'@([^:\s]+)', text)
    results = list(set(results))
    return results


def add_new_comment_to_poll(user_id, poll_id, text):
    try:
        mentions = extract_mention(text)
        for person in mentions:
            person_id = find_id_by_email(person)
            if not check_if_person_is_participant_of_poll_by_id(poll_id, person_id):
                raise Exceptions.UserNotValid
        for person in mentions:
            send_mention_notification(person, poll_id)
        add_comment(user_id, poll_id, text)
    except Exception as e:
        raise e


def add_new_reply_to_comment(user_id, comment_id, text):
    try:
        add_reply(user_id, comment_id, text)
    except Exception as e:
        raise e


def get_comments(poll_id, user_id):
    try:
        comments = get_comments_of_poll(poll_id, user_id)
        return comments
    except Exception as e:
        return e


def remove_comment_from_poll(user_id, comment_id):
    try:
        remove_poll_comment(user_id, comment_id)
    except Exception as e:
        return e


def edit_poll_title(instance, attr, value):
    setattr(instance, attr, value)


def edit_poll_choices(instance, value):
    for choice in instance.choices.iterator():
        instance.choices.remove(choice)
        choice.delete()

    for choice_data in value:
        new_poll = create_choice_time(choice_data)
        instance.choices.add(new_poll)


def edit_poll_participants(instance, value):
    old_participant_emails, new_participant_emails = [], []
    for participant in instance.participants.iterator():
        old_participant_emails.append(participant.email)
        instance.participants.remove(participant)
    for new_participant in value:
        new_participant_emails.append(new_participant.email)
        instance.participants.add(new_participant)
    emails = []
    for new_participant_email in new_participant_emails:
        if new_participant_email not in old_participant_emails:
            emails.append(new_participant_email)
    send_poll_email_to_participants(emails, instance.title, instance.id)