from poll import Exceptions
from poll.data.repo import get_polls, get_choices, add_new_votes_to_poll, add_comment, get_comments_of_poll, add_reply \
    , remove_poll_comment, check_if_person_is_participant_of_poll_by_id, find_id_by_email, create_choice_time, \
    edit_title, add_new_participants, remove_old_participants, remove_not_included_choices, add_new_choices, \
    close_poll, get_participants_emails, get_poll_of_comment, get_comment
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
               + "http://localhost:3000/comments/" + str(poll_id), email)


def add_new_votes(voter, poll_id, votes):
    try:
        return add_new_votes_to_poll(voter, poll_id, votes)
    except Exception as e:
        raise e



def extract_mention(text):
    results = re.findall(r'@([^:\s]+)', text)
    results = list(set(results))
    return results


def check_mention(poll_id, text):
    mentions = extract_mention(text)
    for person in mentions:
        person_id = find_id_by_email(person)
        if not check_if_person_is_participant_of_poll_by_id(poll_id, person_id):
            raise Exceptions.UserNotValid
    thread.start_new_thread(send_mention_notification, (mentions, poll_id))


def add_new_comment_to_poll(user_id, poll_id, text):
    try:
        check_mention(poll_id, text)
        add_comment(user_id, poll_id, text)
    except Exception as e:
        raise e


def add_new_reply_to_comment(user_id, comment_id, text):
    poll = get_poll_of_comment(get_comment(comment_id))
    check_mention(poll.id, text)
    add_reply(user_id, comment_id, text)


def get_comments(poll_id, user_id):
    try:
        comments = get_comments_of_poll(poll_id, user_id)
        return comments
    except Exception as e:
        return e


def remove_comment_from_poll(user, comment_id):
    try:
        remove_poll_comment(user, comment_id)
    except Exception as e:
        return e


def update_poll(validated_data, instance, user):
    for attr, value in validated_data.items():
        if attr == 'title':
            edit_poll_title(instance, attr, value)
        elif attr == 'choices':
            edit_poll_choices(instance, value)
        elif attr == 'participants':
            edit_poll_participants(instance, value, user)
    return instance


def edit_poll_title(instance, attr, value):
    edit_title(instance, attr, value)


def edit_poll_choices(instance, value):
    remove_not_included_choices(instance, value)
    add_new_choices(instance, value)


def edit_poll_participants(instance, participants_value, user):
    old_participant_emails = remove_old_participants(instance)
    new_participant_emails = add_new_participants(instance, participants_value, user)
    send_email_of_update(instance, old_participant_emails, new_participant_emails)


def send_email_of_update(instance, old_participant_emails, new_participant_emails):
    emails = []
    for new_participant_email in new_participant_emails:
        if new_participant_email not in old_participant_emails:
            emails.append(new_participant_email)
    send_poll_email_to_participants(emails, instance.title, instance.id)


def send_poll_close_notification(emails, poll_id):
    send_email("Poll closed", "A poll you were added to in closed:\n"
               "\nYou can view this poll in the following URL:\n"
               + "http://http://localhost:3000/polls/" + poll_id, emails)


def close_poll_by_id(poll_id, user_id):
    close_poll(poll_id, user_id)
    participants = get_participants_emails(poll_id)
    thread.start_new_thread(send_poll_close_notification,
                            (participants, poll_id))
