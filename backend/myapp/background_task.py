from apscheduler.schedulers.background import BackgroundScheduler
from myapp.tasks import your_scheduled_task
import logging

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(your_scheduled_task, 'cron', hour=0, minute=0)
    scheduler.start()
    logging.info("Scheduler started")
