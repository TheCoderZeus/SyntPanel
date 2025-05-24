from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

def schedule_task(name, func, cron):
    scheduler.add_job(func, CronTrigger.from_crontab(cron), id=name, replace_existing=True)

def remove_task(name):
    scheduler.remove_job(name)
