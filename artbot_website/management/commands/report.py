from datetime                    import date, datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.core.mail            import mail_admins, send_mail
from django.conf                 import settings
from artbot_website.models       import Event, Log

class Command(BaseCommand):
    args = 'None.'
    help = 'Generate and email daily crawler report.'

    def handle(self, *args, **options):
        message = ''
        today = date.today()

        new_events = Event.objects.filter(created__contains=today)
        if new_events:
            message += 'New Events\n\n'
            for event in new_events:
                try:
                    message += '%s \t %s\n' % (event.start.date(), event.title)
                except AttributeError:
                    message += '%s \t %s\n' % ('-\t\t', event.title)
        else:
            message += 'No New Events\n'

        unpublished_events = Event.objects.filter(end__gte=today, status=Event.DRAFT_STATUS).order_by('start')
        if unpublished_events:
            message += '\nUnpublished Events\n\n'
            for event in unpublished_events:
                try:
                    message += '%s \t %s\n' % (event.start.date(), event.title)
                except AttributeError:
                    message += '%s \t %s\n' % ('-\t\t', event.title)
        else:
            message += '\nNo Unpublished Events\n'

        error_logs = Log.objects.filter(timestamp__contains=today, level='ERROR')
        if error_logs:
            message += '\nError Logs\n\n'
            for log in error_logs:
                message += '%s \t %s\n' % (log.timestamp.date(), log.message)
        else:
            message += '\nNo Error Logs\n'

        send_mail('Artbot.io Report', message, settings.SERVER_EMAIL, [settings.ADMIN_EMAIL])
