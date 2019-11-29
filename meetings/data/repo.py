from meetings.models import Meeting
from meetings.models import Room
from meetings.models import Participant


def check_if_room_exists(meeting_room):
    return Room.objects.filter(name=meeting_room.room_name).exists()


def create_meeting(meeting_info):
    if not check_if_room_exists(meeting_info.room):
        room = Room(room_name=meeting_info.room)
        room.save()
    room = Room.objects.filter(name=meeting_info.meeting_room.room_name)
    meeting = Meeting(title=meeting_info.title, start_date_time=meeting_info.start_date_time,\
                      end_date_time=meeting_info.end_date_time, room=room)
    for participant in meeting_info.participants:
        person = Participant.objects.filter(name=participant.name, email=participant.email)
        meeting.participants.add(person)

    meeting.save()
