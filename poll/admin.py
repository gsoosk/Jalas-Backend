from django.contrib import admin
from poll.data.models import PollChoiceItem
from poll.data.models import MeetingPoll
from poll.data.models import PollTime


admin.site.register(PollChoiceItem)
admin.site.register(MeetingPoll)
admin.site.register(PollTime)
