from meetings.models import Meeting, Room, Participant
from rest_framework import serializers


class MeetingSerializer(serializers.HyperlinkedModelSerializer):
    participants_id = serializers.ListField(child=serializers.IntegerField())
    room_id = serializers.IntegerField()
    id = serializers.IntegerField(default=-1)
    def set_id(self, id):
        self.id = id
    class Meta:
        model = Meeting
        fields = ('title', 'start_date_time', 'end_date_time', 'room_id', 'participants_id', 'id')


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('room_name', 'capacity', 'location', 'has_video_projector')


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Participant
        fields = ('name', 'email')
