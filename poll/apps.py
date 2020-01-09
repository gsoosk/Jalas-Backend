from django.apps import AppConfig


class PollConfig(AppConfig):
    name = 'poll'

    def ready(self):
        from poll import scheduler
        scheduler.start()
