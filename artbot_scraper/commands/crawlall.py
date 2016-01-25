# -*- coding: utf-8 -*-
from scrapy.commands      import ScrapyCommand
from scrapy.utils.project import get_project_settings
from scrapy.crawler       import CrawlerProcess


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Run all project spiders'

    def run(self, args, opts):
        crawler_process = CrawlerProcess(get_project_settings())

        for spider_name in crawler_process.spider_loader.list():
            spider_cls = crawler_process.spider_loader.load(spider_name)
            crawler_process.crawl(spider_cls)

        crawler_process.start()
