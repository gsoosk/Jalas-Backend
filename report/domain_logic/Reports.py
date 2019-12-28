import datetime
from report.data import repo


class ReportsData:
    __instance = None

    @staticmethod
    def get_instance():
        if ReportsData.__instance is None:
            ReportsData()
        return ReportsData.__instance
        # return repo.get_report()

    def __init__(self):
        if ReportsData.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            report = repo.get_report()
            self.sum_meeting_creation_time = report.sum_meeting_creation_time
            self.num_created_meetings = report.num_created_meetings
            self.num_cancelled_or_modified_meetings = report.num_cancelled_or_modified_meetings
            self.num_reserved_rooms = report.num_reserved_rooms
            self.average_response_time = report.average_response_time
            self.up_time = datetime.datetime.now()
            self.throughput = 0
            self.req_time = {}
            self.reserving = False
            ReportsData.__instance = self

    def add_meeting_creation_time(self, session_key):
        self.req_time[session_key] = datetime.datetime.now()

    def inc_cancelled(self, session_key):
        self.num_cancelled_or_modified_meetings += 1
        repo.increment_cancelled_or_modified()

    def update_average_response(self, response_time):
        repo.update_average_response_time(response_time)
        self.average_response_time = repo.get_average_response_time()

    def finalize_meeting_time(self, session_key):
        creation_time = (datetime.datetime.now() - self.req_time[session_key]).seconds
        self.sum_meeting_creation_time += creation_time
        repo.add_to_creation_time_sum(creation_time)
        self.num_created_meetings += 1
        repo.increment_created_meetings()

    def get_avg_meeting_creation_time(self):
        return self.sum_meeting_creation_time / self.num_created_meetings

    def update_throughput(self):
        if float((datetime.datetime.now() - self.up_time).seconds):
            throughput = float(repo.get_req_count()) / float((datetime.datetime.now() - self.up_time).seconds)
        else:
            throughput = 0
        repo.set_throughput(throughput)
        self.throughput = throughput
        return throughput


