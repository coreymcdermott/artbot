# -*- coding: utf-8 -*-
import os
import sys
import django


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'artbot.settings'

django.setup()

COMMANDS_MODULE  = 'artbot_scraper.commands'
BOT_NAME         = 'artbot_scraper'
SPIDER_MODULES   = ['artbot_scraper.spiders']
NEWSPIDER_MODULE = 'artbot_scraper.spiders'
ITEM_PIPELINES   = {
    'artbot_scraper.pipelines.EventPipeline': 300,
}
