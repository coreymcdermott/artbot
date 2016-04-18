import os
from datetime                    import date, datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from artbot_website.models       import Event, Log

class Command(BaseCommand):
    args = 'None.'
    help = 'Performs housekeeping operations.'

    def handle(self, *args, **options):
        # Delete logs older than retention period.
        hours  = int(os.getenv('LOG_RETENTION', 24))
        cutoff = datetime.now() - timedelta(hours=hours)
        logs   = Log.objects.filter(timestamp__lt=cutoff)
        logs.delete()
        return
