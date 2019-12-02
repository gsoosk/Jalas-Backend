import datetime


class ReportsData:
    __instance = None


    @staticmethod
    def get_instance():
        if ReportsData.__instance is None:
            ReportsData()
        return ReportsData.__instance

    def __init__(self):
        if ReportsData.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.sum_meeting_creation_time = 0
            self.num_created_meetings = 0
            self.num_canceled_or_modified_meetings = 0
            self.num_reserved_rooms = 0
            self.req_time = {}
            self.reserving = False
            ReportsData.__instance = self

    def add_meeting_creation_time(self, session_key):
        self.req_time[session_key] = datetime.datetime.now()

    def inc_canceled(self, session_key):
        self.num_canceled_or_modified_meetings += 1

    def finalize_meeting_time(self, session_key):
        creation_time = (datetime.datetime.now() - self.req_time[session_key]).seconds
        self.sum_meeting_creation_time += creation_time
        self.num_created_meetings += 1

    def get_avg_meeting_creation_time(self):
        return self.sum_meeting_creation_time / self.num_created_meetings


