TIME_ERROR = "End time is before start time!"
ROOM_ERROR = "Given room is not available"

class RoomTimeInvalid(Exception):
    pass

class RoomServiceUnavailable(Exception):
    pass

class RoomServiceInternalError(Exception):
    pass

class RoomIsNotAvailable(Exception):
    pass

class RoomCanNotReserved(Exception):
    pass

class RoomNotFound(Exception):
    pass
