#-*- coding: utf-8 -*-
import re
from scrapy               import Spider
from dateutil             import parser, relativedelta
from artbot_scraper.items import EventItem

class MCASpider(Spider):
    name            = 'MCA'
    allowed_domains = ['mca.com.au']
    start_urls      = ['http://www.mca.com.au/whatson/next-month/']

    def parse(self, response):
        for event in response.xpath('//div[contains(@class, "featured_item")]'):
            item = EventItem()
            item['url']         = 'http://www.mca.com.au' + event.xpath('.//a/@href').extract_first()
            item['venue']       = 'MCA'
            item['title']       = event.xpath('.//h2/text()').extract_first().strip()
            item['description'] = ''.join(event.xpath('.//div[@class="col-md-4"]/p[3]//text()').extract())
            item['image']       = 'http://www.mca.com.au' + event.xpath('.//div[contains(@class, "featured-image")]/@style').re_first('(?<=\().*(?=\))')

            season  = event.xpath('.//b[contains(@class, "occurrence_date")]/text()').extract_first().strip().replace(u'\u2013\xa0', u'')
            match   = re.match('(?P<start>\d+\s+\w+)[\s\-]*(?P<end>\d+\s+\w+)', season)

            if (match):
                start = parser.parse(match.group('start'))
                end   = parser.parse(match.group('end'))

                if (end < start):
                    end = end + relativedelta.relativedelta(years=+1)

                item['start']  = start
                item['end']    = end

            yield item
