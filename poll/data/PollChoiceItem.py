class PollChoiceItemRep:
    def __init__(self, positive_voters, negative_voters, start_time, end_time):
        self.positive_voters = positive_voters
        self.negative_voters = negative_voters
        self.start_time = start_time
        self.end_time = end_time

    def hasSameTime(self, start, end):
        if self.start_time != start:
            return False
        if self.end_time != end:
            return False
        return True

    def toJson(self):
        data = {}
        data['start_time'] = str(self.start_time)
        data['end_time'] = str(self.end_time)
        data['positive_voters'] = self.positive_voters
        data['negative_voters'] = self.negative_voters
        return data
