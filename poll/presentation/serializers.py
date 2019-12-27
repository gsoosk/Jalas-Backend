from rest_framework import serializers
from poll.models import MeetingPoll, Comment
from meetings.models import Participant
from poll.models import PollTime
from poll.data.repo import get_new_poll
from poll.domain_logic.polls_service import send_poll_email_to_participants
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


class CommentSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True, source="user.email")

    class Meta:
        model = Comment
        fields = ['email', 'poll', 'text', 'date_time']


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
        for attr, value in validated_data.items():
            if attr == 'title':
                setattr(instance, attr, value)
            elif attr == 'choices':
                for choice in instance.choices.iterator():
                    instance.choices.remove(choice)
                    choice.delete()

                for choice_data in value:
                    new_poll = PollTime.objects.create(**choice_data)
                    instance.choices.add(new_poll)
            elif attr == 'participants':
                old_participant_emails, new_participant_emails = [], []
                for participant in instance.participants.iterator():
                    old_participant_emails.append(participant.email)
                    instance.participants.remove(participant)
                for new_participant in value:
                    new_participant_emails.append(new_participant.email)
                    instance.participants.add(new_participant)
                emails = []
                for new_participant_email in new_participant_emails:
                    if new_participant_email not in old_participant_emails:
                        emails.append(new_participant_email)
                send_poll_email_to_participants(emails, instance.title, instance.id)

        instance.save()
        return instance

