from rest_framework import serializers


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
