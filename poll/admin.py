from django.contrib import admin
from .models import PollChoiceItem
from .models import MeetingPoll
from .models import PollTime


admin.site.register(PollChoiceItem)
admin.site.register(MeetingPoll)
admin.site.register(PollTime)
