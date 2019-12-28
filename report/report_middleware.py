import datetime

from report.domain_logic.Reports import ReportsData


class ReportMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        curr_time = datetime.datetime.now()

        response = self.get_response(request)

        response_time = (datetime.datetime.now() - curr_time).microseconds
        ReportsData.get_instance().update_average_response(response_time)

        # Code to be executed for each request/response after
        # the view is called.

        return response