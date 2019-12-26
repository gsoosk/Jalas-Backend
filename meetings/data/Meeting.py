class Meeting:
    def __init__(self, title, start_date_time, end_date_time, room, participants, creator, is_cancelled=False):
        self.title = title
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.room = room
        self.creator = creator
        self.participants = participants
        self.is_cancelled = is_cancelled

