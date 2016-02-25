# -*- coding: utf-8 -*-
import re
from scrapy               import Spider
from dateutil             import parser
from artbot_scraper.items import EventItem
from pytz                 import timezone


class MCASpider(Spider):
    name            = 'MCA'
    allowed_domains = ['mca.com.au']
    start_urls      = ['http://www.mca.com.au/whatson/next-month/']

    def parse(self, response):
        for event in response.xpath('//div[contains(@class, "featured_item")]'):
            item                = EventItem()
            item['url']         = 'http://www.mca.com.au' + event.xpath('.//a/@href').extract_first()
            item['venue']       = self.name
            item['title']       = event.xpath('.//h2/text()').extract_first().strip()
            item['description'] = ''.join(event.xpath('.//div[@class="col-md-4"]/p[3]//text()').extract())
            item['image']       = 'http://www.mca.com.au' + event.xpath('.//div[contains(@class, "featured-image")]/@style').re_first('(?<=\().*(?=\))')

            season = event.xpath('.//b[contains(@class, "occurrence_date")]/text()').extract_first().strip().replace(u'\u2013\xa0', u'')
            match  = re.match('(?P<start>\d+\s+\w+)[\s\-]*(?P<end>\d+\s+\w+)', season)

            if (match):
                tz            = timezone('Australia/Sydney')
                item['start'] = tz.localize(parser.parse(match.group('start')))
                item['end']   = tz.localize(parser.parse(match.group('end')))

            yield item
