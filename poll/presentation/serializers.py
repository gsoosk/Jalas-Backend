from rest_framework import serializers
from poll.models import MeetingPoll
from meetings.models import Participant
from poll.models import PollTime
from poll.data.repo import get_new_poll
from poll.domain_logic.polls_service import send_poll_email_to_participants


class MeetingPollSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)


# class PollsSerializer(serializers.Serializer):
#     polls = MeetingPollSerializer(many=True)


class ParticipantSerializer(serializers.Serializer):
    # name = serializers.CharField(max_length=200)
    email = serializers.EmailField()


class PollChoiceItemSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    voters = ParticipantSerializer(many=True)


class PollTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollTime
        fields = ['start_date_time', 'end_date_time']


class ParticipantModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['email']


class PollSerializer(serializers.ModelSerializer):
    choices = PollTimeSerializer(many=True)
    participants = ParticipantModelSerializer(many=True)
    creator_id = serializers.IntegerField(source="creator.id")

    class Meta:
        model = MeetingPoll
        fields = ['title', 'choices', 'creator_id', 'participants']

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        creator_data = validated_data.pop('creator')
        participants_data = validated_data.pop('participants')

        poll, emails = get_new_poll(choices_data, creator_data, participants_data, validated_data.pop('title'))
        send_poll_email_to_participants(emails, poll.title, poll.id)
        return poll
