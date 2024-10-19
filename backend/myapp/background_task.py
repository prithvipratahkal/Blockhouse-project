from apscheduler.schedulers.background import BackgroundScheduler
from myapp.tasks import update_latest_stock_data
from datetime import datetime
import logging

def start():
    scheduler = BackgroundScheduler()
    date_string = '2024-10-19 05:07:00'
    run_date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    scheduler.add_job(update_latest_stock_data, 'date', run_date=run_date)
    scheduler.start()
    logging.info("Scheduler started")
