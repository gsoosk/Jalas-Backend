from meetings.models import Meeting
from meetings.models import Room
from meetings.models import Participant
from meetings import Exceptions


def get_meeting_status_by_id(meeting_id):
    if Meeting.objects.filter(id=meeting_id):
        meeting = Meeting.objects.filter(id=meeting_id)
        return meeting[0].is_cancelled


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
    return meeting.id


def cancel_meeting(meeting_id):
    if Meeting.objects.filter(id=meeting_id):
        meeting = Meeting.objects.filter(id=meeting_id)[0]
        meeting.is_cancelled = True
        meeting.save()
    else:
        raise Exceptions.MeetingNotFound


def check_if_participants_are_valid(participants):
    for participant_id in participants:
        if not Participant.objects.filter(id=participant_id):
            return False

    return True


def get_participants_emails(participants):
    emails = []
    for participant_id in participants:
        person = Participant.objects.filter(id=participant_id)[0]
        emails.append(person.email)
    return emails


def get_meeting_info(meeting_id):
    meeting = Meeting.objects.filter(id=meeting_id)
    return meeting[0]


