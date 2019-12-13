from poll.data.repo import get_polls, get_choices


def get_all_polls_by_creator_name(creator_id):
    try:
        return get_polls(creator_id)
    except Exception as e:
        raise Exception()


def get_poll_details_by_poll_id(poll_id):
    try:
        return get_choices(poll_id)
    except Exception as e:
        raise Exception()

