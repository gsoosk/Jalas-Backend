from meetings.models import Meeting
from meetings.models import Room
from meetings.models import Participant
from meetings.models import Notifications
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
    creator = Participant.objects.filter(id=meeting_info.creator)[0]
    room = Room.objects.filter(room_name=meeting_info.room.room_name).first()
    meeting = Meeting(title=meeting_info.title, start_date_time=meeting_info.start_date_time,
                      end_date_time=meeting_info.end_date_time, room=room, creator=creator)
    meeting.save()
    for participant_id in meeting_info.participants:
        if Participant.objects.filter(id=participant_id):
            person = Participant.objects.filter(id=participant_id)[0]
        meeting.participants.add(person)

    meeting.save()
    return meeting.id


def cancel_meeting(meeting_id, user_id):
    if Meeting.objects.filter(id=meeting_id):
        meeting = Meeting.objects.filter(id=meeting_id)[0]
        if meeting.creator.id == user_id:
            meeting.is_cancelled = True
            meeting.save()
        else:
            raise Exceptions.UnauthorizedUser
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


def get_meeting_info(meeting_id, user_id):
    if not Meeting.objects.filter(id=meeting_id).exists():
        raise Exceptions.MeetingNotExists
    meeting = Meeting.objects.filter(id=meeting_id)[0]
    participants = meeting.participants
    creator = meeting.creator
    if (is_user_in_meeting(participants, user_id)) or (creator.id == user_id):
        return meeting
    else:
        raise Exceptions.UnauthorizedUser


def get_owner_notifications(user_id):
    if not Participant.objects.filter(id=user_id):
        raise Exceptions.InvalidParticipantInfo
    user = Participant.objects.filter(id=user_id)[0]
    notifications = Notifications.objects.filter(owner=user)[0]
    return notifications


def update_notifications_fields(notifications, request):
    notifications.poll_creator_vote_notifications = request.data['poll_creator_vote_notifications']
    notifications.poll_contribution_invitation = request.data['poll_contribution_invitation']
    notifications.mention_notification = request.data['mention_notification']
    notifications.poll_close_notification = request.data['poll_close_notification']
    notifications.meeting_set_creator_notification = request.data['meeting_set_creator_notification']
    notifications.meeting_invitation = request.data['meeting_invitation']
    notifications.cancel_meeting_notification = request.data['cancel_meeting_notification']

def get_emails(participants):
    emails = []
    for participant in participants.iterator():
        emails.append(participant.email)
    return emails


def is_user_in_meeting(participants, user_id):
    try:
        for participant in participants.iterator():
            if participant.id == user_id:
                return True
        return False
    except:
        return False


def get_meetings_by_id(user_id):
    user_meetings = []
    meetings = Meeting.objects.all()
    for meeting in meetings:
        participants = meeting.participants
        creator = meeting.creator
        if (is_user_in_meeting(participants, user_id)) or (creator.id == user_id):
            user_meetings.append(meeting)
    output = {'user_id': user_id, 'meetings': [{'title': m.title, 'id': m.id} for m in user_meetings]}
    return output


def get_all_meetings():
    return Meeting.objects.all()
