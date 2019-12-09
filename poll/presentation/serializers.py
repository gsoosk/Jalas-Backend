from rest_framework import serializers
from poll.models import MeetingPoll
from meetings.models import Participant
from poll.models import PollTime
from meetings.presentation.serializers import ParticipantSerializer


class MeetingPollSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)


# class PollsSerializer(serializers.Serializer):
#     polls = MeetingPollSerializer(many=True)


class ParticipantSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()


class PollChoiceItemSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    voters = ParticipantSerializer(many=True)


class PollTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollTime
        fields =['start_date_time', 'end_date_time']


class PollSerializer(serializers.ModelSerializer):
    choices = PollTimeSerializer(many=True)
    creator = ParticipantSerializer()

    class Meta:
        model = MeetingPoll
        fields = ['title', 'choices', 'creator']

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        creator_data = validated_data.pop('creator')
        creator = Participant.objects.create(**creator_data)
        poll = MeetingPoll.objects.create(creator=creator, title=validated_data.pop('title'))

        for choice_data in choices_data:
            new_poll = PollTime.objects.create(**choice_data)
            poll.choices.add(new_poll)
        return poll