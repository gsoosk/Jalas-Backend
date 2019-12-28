# from django.http import HttpResponseNotFound, HttpResponse
#
#
# class CheckValidParamMixin(object):
#
#     def dispatch(self, request, *args, **kwargs):
#         param = self.kwargs.get('param')
#         valid_param = is_valid_param(param)
#         if valid_param:
#             return super(CheckValidParamMixin, self).dispatch(request, *args, **kwargs)
#         return HttpResponseNotFound('Invalid param')
#
#
# class LogSuccessResponse(HttpResponse):
#
#     def close(self):
#         super(LogSuccessResponse, self).close()
#         # do whatever you want, this is the last codepoint in request handling
#         if self.status_code == 200:
#             print('HttpResponse successful: %s' % self.status_code)
