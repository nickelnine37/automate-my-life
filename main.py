from notion.birthdays import send_birthday_notifications
from notion.calendar import send_event_notifications
from notion.reminders import get_reminder_notifications

from apscheduler.schedulers.blocking import BlockingScheduler


class Scheduler:

    def __init__(self):

        self.scheduler = BlockingScheduler()
        self.refresh()
        self.scheduler.add_job(self.refresh, trigger='cron', hour=0, minute=0)


    def refresh(self):

        self.scheduler.remove_all_jobs()

        self.scheduler.add_job(send_birthday_notifications, trigger='cron', hour=12, minute=0)
        self.scheduler.add_job(send_event_notifications, trigger='cron', hour=9, minute=0)

        self.reminder_notifications = get_reminder_notifications()

        for notification, cron_job in self.reminder_notifications:

            try:
                self.scheduler.add_job(notification.send, trigger='cron', **cron_job)
            except:
                print(cron_job)

        print(self.scheduler.print_jobs())



    def start(self):
        self.scheduler.start()


if __name__ == '__main__':

    scheduler = Scheduler()
    scheduler.start()



