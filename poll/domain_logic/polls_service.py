
from poll.data.repo import get_polls, get_choices


def get_all_polls_by_creator_name(creator_id):
    return get_polls(creator_id)


def get_poll_details(poll_id):
    return get_choices(poll_id)

