from rest_framework import serializers
from poll.models import MeetingPoll, Comment, Reply
from meetings.models import Participant
from poll.models import PollTime
from poll.data.repo import get_new_poll
from poll.domain_logic.polls_service import send_poll_email_to_participants, edit_poll_title, edit_poll_choices, \
    edit_poll_participants, update_poll
import poll.Exceptions as Exceptions


class MeetingPollSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)


# class PollsSerializer(serializers.Serializer):
#     polls = MeetingPollSerializer(many=True)


class ParticipantSerializer(serializers.Serializer):
    # name = serializers.CharField(max_length=200)
    email = serializers.EmailField()


class PollChoiceItemSerializer(serializers.Serializer):
    # voter
    # poll
    # chosen_time
    # agrees
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


class ReplyCommentSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True, source="user.email")

    class Meta:
        model = Reply
        fields = ['email', 'text', 'date_time']


class CommentSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True, source="user.email")
    replies = ReplyCommentSerializer(many=True)

    class Meta:
        model = Comment
        fields = ['id', 'email', 'poll', 'text', 'date_time', 'replies']


class PollSerializer(serializers.ModelSerializer):
    choices = PollTimeSerializer(many=True)
    participants = serializers.SlugRelatedField(many=True, slug_field='email', queryset=Participant.objects.all())
    creator_id = serializers.IntegerField(source="creator.id", read_only=True)
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MeetingPoll
        fields = ['id','title', 'choices', 'creator_id', 'participants']

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        creator = self.context['request'].user
        participants = validated_data.pop('participants')
        try:
            poll, emails = get_new_poll(choices_data, creator, participants, validated_data.pop('title'))
        except Exceptions.ParticipantsAreNotExsits:
            raise serializers.ValidationError('Some of Participants Are Not Exists')
        send_poll_email_to_participants(emails, poll.title, poll.id)
        return poll

    def update(self, instance, validated_data):
        return update_poll(validated_data, instance)

