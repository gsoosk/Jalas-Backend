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
        creator = Participant.objects.get(pk=creator_data['id'])
        poll = MeetingPoll.objects.create(creator=creator, title=validated_data.pop('title'))

        for choice_data in choices_data:
            new_poll = PollTime.objects.create(**choice_data)
            poll.choices.add(new_poll)

        for participant_data in participants_data:
            new_participant = Participant.objects.create(**participant_data)
            poll.participants.add(new_participant)

        return poll
