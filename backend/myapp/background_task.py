from apscheduler.schedulers.background import BackgroundScheduler
from myapp.tasks import update_latest_stock_data
import logging

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_latest_stock_data, 'cron', hour=0, minute=0)
    scheduler.start()
    logging.info("Scheduler started")
