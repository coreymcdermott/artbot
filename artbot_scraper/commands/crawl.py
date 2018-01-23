# -*- coding: utf-8 -*-
import logging
from scrapy.commands                 import ScrapyCommand
from scrapy.exceptions               import UsageError
from scrapy.utils.log                import configure_logging
from artbot_website.logging_handlers import DatabaseLogHandler


class Command(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return "[options] <spider>"

    def short_desc(self):
        return "Run a spider"

    def run(self, args, opts):
        if len(args) < 1:
            raise UsageError()
        elif len(args) > 1:
            raise UsageError("running 'scrapy crawl' with more than one spider is no longer supported")
        spider_name = args[0]

        configure_logging(install_root_handler=False)
        logger = logging.getLogger()
        databaseLogHandler = DatabaseLogHandler()
        logger.addHandler(databaseLogHandler)

        self.crawler_process.crawl(spider_name)
        self.crawler_process.start()
