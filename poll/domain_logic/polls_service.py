from poll.data.repo import get_polls, get_choices, add_new_votes_to_poll
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
    thread.start_new_thread(send_email, ("Poll Contribution Invitation", "There is a poll named "+title+" you added to it in Jalas"
               + "\nYou can view this Poll in the following URL :\n"
               + "http://" + "localhost" + ":" + "3000" + "/polls/" + str(poll_id), emails))


def add_new_votes(voter, poll_id, votes):
    try:
        add_new_votes_to_poll(voter, poll_id, votes)
    except Exception as e:
        raise e
