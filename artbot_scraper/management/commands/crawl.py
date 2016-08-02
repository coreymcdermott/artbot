# -*- coding: utf-8 -*-
from __future__                  import absolute_import
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('crawler')

    def handle(self, *args, **options):
        from scrapy.cmdline import execute
        if options['crawler'] == 'all':
            execute(['scrapy', 'all'])
        else:
            execute(['scrapy', 'crawl', options['crawler']])
