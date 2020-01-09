from apscheduler.schedulers.background import BackgroundScheduler
from poll.data import repo
from poll.domain_logic import polls_service
from threading import Lock, Thread
lock = Lock()


def close_with_deadline_polls():
    lock.acquire()
    polls = repo.get_polls_to_schedule()
    print('Closing ' + str(polls))
    for poll in polls:
        polls_service.close_poll_if_needed(poll)
    lock.release()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(close_with_deadline_polls, 'interval', minutes=1)
    scheduler.start()
