from meetings.models import Meeting, Room, Participant, Notifications
from rest_framework import serializers


class MeetingSerializer(serializers.HyperlinkedModelSerializer):
    participants_id = serializers.ListField(child=serializers.IntegerField())
    room_id = serializers.IntegerField()
    id = serializers.IntegerField(default=-1)

    def set_id(self, id):
        self.id = id

    class Meta:
        model = Meeting
        fields = ['title', 'start_date_time', 'end_date_time', 'room_id', 'participants_id', 'id']

class SignupSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField(max_length=200)
    is_staff = serializers.BooleanField()


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ['room_name', 'capacity', 'location', 'has_video_projector']


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Participant
        fields = ['email']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['poll_creator_vote_notifications', 'poll_contribution_invitation', 'mention_notification',
                  'poll_close_notification', 'meeting_set_creator_notification', 'meeting_invitation',
                  'cancel_meeting_notification']


class MeetingInfoSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)
    room = RoomSerializer(many=False)
    creator = ParticipantSerializer(many=False)

    class Meta:
        model = Meeting
        fields = ['id', 'title', 'start_date_time', 'end_date_time', 'room', 'participants', 'is_cancelled', 'creator']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = Participant
        fields = ['email', 'password']
