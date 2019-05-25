# -*- coding: utf-8 -*-
import re
import json
from datetime             import datetime
from scrapy               import Spider
from dateutil             import parser
from artbot_scraper.items import EventItem
from pytz                 import timezone
from scrapy.utils.response import open_in_browser

class MCASpider(Spider):
    name            = 'MCA'
    allowed_domains = ['mca.com.au']
    start_urls      = ['https://www.mca.com.au/api/query-whats-on/?show=exhibitions&on=next-thirty-days&for=everyone']

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())

        for exhibition in json_response['exhibitions']:
            item                = EventItem()
            item['url']         = exhibition['url']
            item['venue']       = self.name
            item['title']       = exhibition['title']
            item['description'] = exhibition['summary']
            item['image']       = response.urljoin(exhibition['thumbnail']['src'])

            match  = re.match('until (?P<end>\d+\s+\w+)', exhibition['date_range'].replace('&nbsp;', ' '))

            if (match):
                tz            = timezone('Australia/Sydney')
                item['start'] = tz.localize(datetime.today())
                item['end']   = tz.localize(parser.parse(match.group('end')))

            yield item
