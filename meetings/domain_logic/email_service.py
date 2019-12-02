from meetings import Exceptions
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings


def send_email(subject, message, receiver):
    subject = subject
    body = message
    to = receiver

    try:
        send_mail(
            subject,
            body,
            settings.EMAIL_FROM,
            to,
            fail_silently=False,
        )
    except BadHeaderError:
        return Exceptions.EmailCouldNotBeSent()
