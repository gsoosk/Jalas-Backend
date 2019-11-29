from django.contrib import admin

from .models import Meeting
from .models import Room
from .models import Participant


admin.site.register(Meeting)
admin.site.register(Room)
admin.site.register(Participant)
