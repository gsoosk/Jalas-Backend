from django.core.management.base import BaseCommand, CommandError
from reports.domain_logic.Reports import ReportsData


class Command(BaseCommand):
    def handle(self, *args, **options):
        report = ReportsData.get_instance()
        average = 0
        if report.num_created_meetings > 0:
            average = report.sum_meeting_creation_time/report.num_created_meetings
        print("Average Creation Time: " + str(average))
        print("Number of reserved rooms: " + str(report.num_reserved_rooms))
        print("Number of cancelled/modified meetings: " + str(report.num_canceled_or_modified_meetings))
