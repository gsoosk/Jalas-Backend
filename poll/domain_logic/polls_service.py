
from poll.data.models import MeetingPoll


def get_all_polls_by_creator_name(creator_name):
    # return ""
    polls = MeetingPoll.objects.filter(creator__name=creator_name).select_related()
    return polls

# def get_polls_details(poll):
#     choices =

