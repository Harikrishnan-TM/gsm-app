import os
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command

def start():
    if os.environ.get('RUN_MAIN') != 'true':  # ✅ Only run in the main process
        return

    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: call_command('simulate_market'), 'interval', minutes=5)
    scheduler.start()
    print("✅ Scheduler started")
