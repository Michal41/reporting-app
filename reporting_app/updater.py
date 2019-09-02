from .report import Report
from apscheduler.schedulers.background import BackgroundScheduler

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(Report.send_report, 'cron', hour="21")
    scheduler.start()
