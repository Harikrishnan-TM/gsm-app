from django.core.management.base import BaseCommand
import time
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Continuously runs simulate_market every 5 minutes.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting price simulation loop (every 5 minutes)...")
        while True:
            self.stdout.write("Running simulate_market...")
            call_command('simulate_market')
            self.stdout.write("Sleeping for 5 minutes...")
            time.sleep(300)  # 300 seconds = 5 minutes
