from poll.data.repo import get_polls, get_choices, add_new_votes_to_poll, add_comment, get_comments_of_poll, add_reply\
    , remove_poll_comment
from meetings.domain_logic.email_service import send_email
import _thread as thread


def get_all_polls_by_creator_name(creator_id):
    try:
        return get_polls(creator_id)
    except Exception as e:
        raise Exception()


def get_poll_details_by_poll_id(poll_id):
    try:
        return get_choices(poll_id)
    except Exception as e:
        raise e


def send_poll_email_to_participants(emails, title, poll_id):
    thread.start_new_thread(send_email, (
        "Poll Contribution Invitation", "You have been invited to a poll called " + title + " in Jalas"
        + "\nYou can view this poll using the URL below:\n"
        + "http://" + "localhost" + ":" + "3000" + "/polls/" + str(poll_id), emails))


def add_new_votes(voter, poll_id, votes):
    try:
        add_new_votes_to_poll(voter, poll_id, votes)
    except Exception as e:
        raise e


def add_new_comment_to_poll(user_id, poll_id, text):
    try:
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