from datetime                    import date, datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from artbot_website.models       import Event, Log

class Command(BaseCommand):
    args = 'None.'
    help = 'Performs housekeeping operations.'

    def handle(self, *args, **options):
        # Delete logs older than 3 days.
        cutoff = datetime.now() - timedelta(days=3)
        logs   = Log.objects.filter(timestamp__lt=cutoff)
        logs.delete()
        return
