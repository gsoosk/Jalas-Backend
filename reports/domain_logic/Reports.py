class Reports:
    __instance = None

    @staticmethod
    def get_instance():
        if Reports.__instance is None:
            Reports()
        return Reports.__instance

    def __init__(self):
        if Reports.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.sum_meeting_creation_time = 0
            self.num_created_meetings = 0
            self.num_canceled_or_modified_meetings = 0
            self.num_reserved_rooms = 0
            self.req_time = {}
            Reports.__instance = self

    # def add_meeting_creation_time(self, request):
    #     self.req_time[request.]

