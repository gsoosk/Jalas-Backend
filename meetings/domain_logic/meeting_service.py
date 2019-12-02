from meetings.data.Room import Room
from meetings.data.repo import create_meeting
import requests
import json
from meetings import Exceptions
from meetings.domain_logic.email_service import send_email


def is_time_valid(start, end):
    return end > start


def send_reserve_request(start, end, room_name):
    while True:
        try:
            available_rooms = requests.post('http://213.233.176.40/rooms/' + str(room_name) + '/reserve', json={
                                            "username": "rkhosravi",
                                            "start": start[:-1],
                                            "end": end[:-1],
                                            })
            if available_rooms.status_code == 404:
                raise Exceptions.RoomCanNotBeReserved()
            if available_rooms.status_code == 400:
                raise Exceptions.RoomTimeInvalid()
            elif available_rooms.status_code == 503:
                raise Exceptions.RoomServiceUnavailable()
            elif available_rooms.status_code == 500:
                raise Exceptions.RoomServiceInternalError()
            elif available_rooms.status_code == 200:
                return
        except Exceptions.RoomCanNotBeReserved as e:
            raise e
        except Exceptions.RoomTimeInvalid as e:
            raise e
        except:
            pass


def get_available_rooms_service(start, end):
    while True:
        try:
            available_rooms = requests.get(url='http://213.233.176.40/available_rooms' +
                                               '?start=' + start[:-1] + '&end=' + end[:-1])
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
        except:
            pass


def reserve_room(start, end, room):
    rooms = get_available_rooms_service(start, end)
    if room.room_name not in rooms.keys():
        raise Exceptions.RoomIsNotAvailable()
    send_reserve_request(start, end, room.room_name)


def create_new_meeting(new_meeting):
    if not is_time_valid(new_meeting.start_date_time, new_meeting.end_date_time):
        raise Exceptions.RoomTimeInvalid(Exceptions.TIME_ERROR)
    reserve_room(new_meeting.start_date_time, new_meeting.end_date_time, new_meeting.room)
    send_email("Meeting Invitation", "There is going to be a meeting with following information:\nTime:"
                                     + str(new_meeting.start_date_time) + " - " + str(new_meeting.end_date_time) +
                                     "\nRoom: " + str(new_meeting.room.room_name) + "\n", ["qsoosk@gmail.com,"])
    create_meeting(new_meeting)
