class Room:
    def __init__(self, room_name, capacity=0, location="", has_video_projector=False):
        self.room_name = room_name
        self.capacity = capacity
        self.location = location
        self.has_video_projector = has_video_projector
