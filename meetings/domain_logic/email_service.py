from django.core.mail import send_mail
from django.conf import settings


def send_email(subject, message, sender, receiver):
    # try:
    #     send_mail(
    #         subject,
    #         message,
    #         sender,
    #         [receiver],
    #         fail_silently=False,
    #     )

    # except Exception as e:
    return
