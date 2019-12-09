from rest_framework import serializers
from poll.models import MeetingPoll
from poll.models import PollTime
from meetings.presentation.serializers import ParticipantSerializer


class MeetingPollSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)


# class PollsSerializer(serializers.Serializer):
#     polls = MeetingPollSerializer(many=True)


class ParticipantSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)


class PollChoiceItemSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    voters = ParticipantSerializer(many=True)


class PollTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollTime
        fields =['start_date_time', 'end_date_time']


class PollSerializer(serializers.ModelSerializer):
    times = PollTimeSerializer(many=True)
    creator = ParticipantSerializer(many=True)
    class Meta:
        model = MeetingPoll
        fields = ['title', 'times', 'creator']
