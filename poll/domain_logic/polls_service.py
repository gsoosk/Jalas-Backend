
from poll.data.repo import get_polls, get_choices


def get_all_polls_by_creator_name(creator_name):
    return get_polls(creator_name)


def get_poll_details(poll_title):
    return get_choices(poll_title)

