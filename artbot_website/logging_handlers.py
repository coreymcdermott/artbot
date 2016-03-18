import logging
import datetime
import pytz

class DatabaseLogHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        try:
            from artbot_website.models import Log
            log = Log(level=record.levelname, message=record.message)
            log.save()
        except:
            raise

        return