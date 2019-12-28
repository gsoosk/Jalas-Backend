from django.contrib import admin
from poll.models import PollChoiceItem
from poll.models import MeetingPoll
from poll.models import PollTime
from poll.models import Comment
from poll.models import Reply


admin.site.register(PollChoiceItem)
admin.site.register(MeetingPoll)
admin.site.register(PollTime)
admin.site.register(Comment)
admin.site.register(Reply)