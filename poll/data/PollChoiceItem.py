class PollChoiceItem:
    def __init__(self, voters, start_time, end_time):
        self.voters = voters
        self.start_time = start_time
        self.end_time = end_time

    def hasSameTime(self, start, end):
        if self.start_time != start:
            return False
        if self.end_time != end:
            return False
        return True
