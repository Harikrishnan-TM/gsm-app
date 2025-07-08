# stocks/scheduler.py

import os
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
import logging

def start():
    # Prevent scheduler from running twice in development mode
    if os.environ.get('RUN_MAIN') != 'true':
        return

    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: call_command('simulate_market'), 'interval', minutes=5)
    scheduler.start()

    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    print("✅ Stock simulation scheduler started.")
