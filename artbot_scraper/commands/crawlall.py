# -*- coding: utf-8 -*-
import logging
from scrapy.commands                import ScrapyCommand
from scrapy.utils.project           import get_project_settings
from scrapy.crawler                 import CrawlerProcess
from scrapy.utils.log               import configure_logging
from artbot_website.loggingHandlers import DatabaseLogHandler


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Run all project spiders'

    def run(self, args, opts):
        crawler_process = CrawlerProcess(get_project_settings())

        configure_logging(install_root_handler=False)
        logger = logging.getLogger()
        databaseLogHandler = DatabaseLogHandler()
        logger.addHandler(databaseLogHandler)

        for spider_name in crawler_process.spider_loader.list():
            spider_cls = crawler_process.spider_loader.load(spider_name)
            crawler_process.crawl(spider_cls)

        crawler_process.start()
