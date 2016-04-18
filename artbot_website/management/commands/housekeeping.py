import os
from datetime                    import date, datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from artbot_website.models       import Event, Log
from django.contrib.admin.models import LogEntry


class Command(BaseCommand):
    args = 'None.'
    help = 'Performs housekeeping operations.'

    def handle(self, *args, **options):
        # Calculate retention cutofff.
        hours  = int(os.getenv('LOG_RETENTION', 24))
        cutoff = datetime.now() - timedelta(hours=hours)

        # Delete artbot_website logs older than retention period.
        logs = Log.objects.filter(timestamp__lt=cutoff)
        logs.delete()

        # Delete Django Admin logs older than retention period.
        logEntries = LogEntry.objects.filter(action_time__lt=cutoff)
        logEntries.delete()
        return
