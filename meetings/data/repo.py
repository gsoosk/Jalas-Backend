from meetings.models import Meeting
from meetings.models import Room
from meetings.models import Participant


def check_if_room_exists(meeting_room):
    return Room.objects.filter(room_name=meeting_room.room_name).exists()


def create_meeting(meeting_info):
    if not check_if_room_exists(meeting_info.room):
        room = Room(room_name=meeting_info.room.room_name)
        room.save()
    room = Room.objects.filter(room_name=meeting_info.room.room_name).first()
    meeting = Meeting(title=meeting_info.title, start_date_time=meeting_info.start_date_time,
                      end_date_time=meeting_info.end_date_time, room=room)
    meeting.save()
    for participant_id in meeting_info.participants:
        if Participant.objects.filter(id=participant_id):
            person = Participant.objects.filter(id=participant_id)[0]
        meeting.participants.add(person)

    meeting.save()
