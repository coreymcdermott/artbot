# -*- coding: utf-8 -*-
import re
from scrapy               import Spider
from dateutil             import parser
from artbot_scraper.items import EventItem
from pytz                 import timezone


class NationalArtSchoolSpider(Spider):
    name            = 'National Art School'
    allowed_domains = ['nas.edu.au']
    start_urls      = ['http://www.nas.edu.au/current-exhibitions/']

    def parse(self, response):
        item                = EventItem()
        item['url']         = response.url
        item['venue']       = self.name
        item['title']       = response.xpath('.//h2/text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('//div//em/parent::div//text()').extract()).strip()
        item['image']       = response.urljoin(response.xpath('.//img[contains(@class, "vc_single_image-img")]/@src').extract_first())

        season = response.xpath('//div[contains(@class, "vc_empty_space")]//strong/parent::div/text()[1]').extract_first()
        match  = re.search(u'(?P<start>[\w\d\s]+)\s\—\s(?P<end>[\w\d\s]+)', season)

        if (match):
            tz            = timezone('Australia/Sydney')
            item['start'] = tz.localize(parser.parse(match.group('start')))
            item['end']   = tz.localize(parser.parse(match.group('end')))

        yield item
