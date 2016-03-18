# -*- coding: utf-8 -*-
import logging
from scrapy.commands                import ScrapyCommand
from scrapy.utils.log               import configure_logging
from artbot_website.logging_handlers import DatabaseLogHandler


class Command(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Run all project spiders'

    def run(self, args, opts):
        configure_logging(install_root_handler=False)
        logger = logging.getLogger()
        databaseLogHandler = DatabaseLogHandler()
        logger.addHandler(databaseLogHandler)

        for spider_name in self.crawler_process.spider_loader.list():
            spider_class = self.crawler_process.spider_loader.load(spider_name)
            self.crawler_process.crawl(spider_class)

        self.crawler_process.start()
