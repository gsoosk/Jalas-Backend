from django.db import models


class Report(models.Model):
    sum_meeting_creation_time = models.FloatField(default=0)
    num_created_meetings = models.IntegerField(default=0)
    num_cancelled_or_modified_meetings = models.IntegerField(default=0)
    num_reserved_rooms = models.IntegerField(default=0)
    average_response_time = models.FloatField(default=0)
    throughput = models.IntegerField(default=0)
    req_count = models.IntegerField(default=0)
    # req_time = models.
    # reserving = models.BooleanField(default=False)
