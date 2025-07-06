from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: call_command('simulate_market'), 'interval', minutes=5)
    scheduler.start()
