from report.models import Report


def get_report():
    reports = Report.objects.all()
    if len(reports) == 0:
        report = Report.objects.create()
        report.save()
    return Report.objects.all()[0]


def increment_cancelled_or_modified():
    report = get_report()
    report.num_cancelled_or_modified_meetings += 1
    report.save()


def increment_reserved():
    report = get_report()
    report.num_reserved_rooms += 1
    report.save()


def increment_created_meetings():
    report = get_report()
    report.num_reserved_rooms += 1
    report.save()


def add_to_creation_time_sum(sum):
    report = get_report()
    report.sum_meeting_creation_time += sum
    report.save()


def get_average_response_time():
    report = get_report()
    return report.average_response_time


def get_average_creation_time():
    report = get_report()
    return report.sum_meeting_creation_time / report.num_created_meetings


def update_average_response_time(time):
    report = get_report()
    new_sum = report.average_response_time * report.req_count + time
    report.req_count += 1
    report.average_response_time = new_sum / report.req_count
    report.save()
