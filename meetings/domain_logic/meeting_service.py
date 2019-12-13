from meetings.data.Room import Room
import requests
import json
from meetings import Exceptions
from meetings.domain_logic.email_service import send_email
import _thread as thread
from reports.domain_logic.Reports import ReportsData
from meetings.data.repo import create_meeting, cancel_meeting, get_meeting_status_by_id, \
    check_if_participants_are_valid, get_participants_emails, get_meeting_info


def is_time_valid(start, end):
    return end > start


def cancel_room_reservation(meeting_id):
    cancel_meeting(meeting_id)
    # cancel_numbers += 1


def send_reserve_request(start, end, room_name):
    while True:
        try:
            available_rooms = requests.post('http://5.253.27.176/rooms/' + str(room_name) + '/reserve', json={
                "username": "rkhosravi",
                "start": start[:19],
                "end": end[:19],
            }, timeout=2)
            if available_rooms.status_code == 404:
                raise Exceptions.RoomCanNotBeReserved()
            if available_rooms.status_code == 400:
                raise Exceptions.RoomTimeInvalid()
            elif available_rooms.status_code == 503:
                raise Exceptions.RoomServiceUnavailable()
            elif available_rooms.status_code == 500:
                raise Exceptions.RoomServiceInternalError()
            elif available_rooms.status_code == 200:
                report = ReportsData.get_instance()
                report.num_reserved_rooms += 1
                return
        except Exceptions.RoomCanNotBeReserved as e:
            raise e
        except Exceptions.RoomTimeInvalid as e:
            raise e
        except requests.Timeout as e:
            raise e
        except:
            pass


def get_available_rooms_service(start, end):
    while True:
        try:
            available_rooms = requests.get(url='http://5.253.27.176/available_rooms' +
                                               '?start=' + start[:19] + '&end=' + end[:19], timeout=3)
            if available_rooms.status_code == 400:
                response = json.loads(available_rooms.text)
                raise Exceptions.RoomTimeInvalid(response['message'])
            elif available_rooms.status_code == 503:
                raise Exceptions.RoomServiceUnavailable()
            elif available_rooms.status_code == 500:
                raise Exceptions.RoomServiceInternalError()
            elif available_rooms.status_code == 200:
                rooms = {}
                rooms_name = json.loads(available_rooms.text)['availableRooms']
                for room_name in rooms_name:
                    new_room = Room(room_name)
                    rooms[room_name] = new_room
                return rooms
        except Exceptions.RoomTimeInvalid as e:
            raise e
        except requests.Timeout as e:
            raise e
        except:
            pass


def reserve_room(start, end, room):
    rooms = get_available_rooms_service(start, end)
    if room.room_name not in rooms.keys():
        raise Exceptions.RoomIsNotAvailable()
    send_reserve_request(start, end, room.room_name)


def check_participants_valid(participants):
    if check_if_participants_are_valid(participants):
        return
    raise Exceptions.InvalidParticipantInfo()


def send_email_to_creator(start, end, room_name):
    send_email("Meeting Notification", "There is going to be a meeting with following information:\nTime:"
               + start + " - "
               + end + "\nRoom: "
               + room_name + "\n", ["qsoosk@gmail.com"])


def send_email_to_participants(start, end, room_name, participants, host, port, meeting_id):
    emails = get_participants_emails(participants)
    send_email("Meeting Invitation", "There is going to be a meeting with following information:\nTime:"
               + start + " - "
               + end + "\nRoom: "
               + room_name + "\nYou can view this meeting in the following URL:\n"
               + "http://" + host + ":" + port + "/meetings/" + meeting_id, emails)


def send_email_thread(start, end, room_name, participants, host, port, meeting_id):
    send_email_to_creator(start, end, room_name)
    send_email_to_participants(start, end, room_name, participants, host, port, meeting_id)


def reserve_until_cancel(start, end, room_name, meeting_id):
    ReportsData.get_instance().reserving = True
    while not get_meeting_status_by_id(meeting_id):
        try:
            reserve_room(start, end, room_name)
            break
        except requests.Timeout as e:
            pass
        except e:
            ReportsData.get_instance().reserving = False
            raise e
    print("reserved")
    ReportsData.get_instance().reserving = False


def create_new_meeting(new_meeting, host, port):
    if not is_time_valid(new_meeting.start_date_time, new_meeting.end_date_time):
        raise Exceptions.RoomTimeInvalid(Exceptions.TIME_ERROR)
    check_participants_valid(new_meeting.participants)
    meeting_id = create_meeting(new_meeting)
    # Sending Mail
    thread.start_new_thread(send_email_thread, (str(new_meeting.start_date_time), str(new_meeting.end_date_time),
                                                str(new_meeting.room.room_name), new_meeting.participants, host, port,
                                                str(meeting_id)))
    # Reserving
    try:
        reserve_room(new_meeting.start_date_time, new_meeting.end_date_time, new_meeting.room)
        return meeting_id, True
    except requests.Timeout as e:
        thread.start_new_thread(reserve_until_cancel,
                                (new_meeting.start_date_time, new_meeting.end_date_time, new_meeting.room, meeting_id))
        return meeting_id, False


def get_meeting_details_by_poll_id(meeting_id):
    return get_meeting_info(meeting_id)
