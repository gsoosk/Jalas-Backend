EMAIL_ERROR = "Your email is not in system"
PARTICIPANT_ERROR = "You are not allowed to vote for this poll"
POLL_ERROR = "Poll ID is not valid"
TIME_ERROR = "Time is invalid for this poll"
VOTED_BEFORE_ERROR = "You have voted before for this poll"


class InvalidEmail(Exception):
    pass


class InvalidPoll(Exception):
    pass


class InvalidComment(Exception):
    pass


class NotParticipant(Exception):
    pass


class InvalidChosenTime(Exception):
    pass


class VotedBefore(Exception):
    pass


class ParticipantsAreNotExsits(Exception):
    pass


class InvalidPoll(Exception):
    pass


class AccessDenied(Exception):
    pass


class PollNotExists(Exception):
    pass


class UserNotValid(Exception):
    pass


class AlreadyClosed(Exception):
    pass


class CanChangePoll(Exception):
    pass


class PollClosed(Exception):
    pass


class NoChoiceCanNotSelectToClose(Exception):
    pass