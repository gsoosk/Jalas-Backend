
class PollChoiceItemRep:
    def __init__(self, _id, positive_voters, negative_voters, agree_ifneeded_voters, start_time, end_time):
        self._id = _id
        self.positive_voters = positive_voters
        self.negative_voters = negative_voters
        self.agree_ifneeded_voters = agree_ifneeded_voters
        self.start_time = start_time
        self.end_time = end_time

    def hasSameTime(self, start, end):
        if self.start_time != start:
            return False
        if self.end_time != end:
            return False
        return True

    def toJson(self):
        data = {'id': self._id, 'start_time': ('T'.join(str(self.start_time).split(' '))),
                'end_time': ('T'.join(str(self.end_time).split(' '))), 'positive_voters': self.positive_voters,
                'negative_voters': self.negative_voters, 'agree_ifneeded_voters': self.agree_ifneeded_voters}
        return data
