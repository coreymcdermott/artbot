# -*- coding: utf-8 -*-
import re
from scrapy               import Spider
from dateutil             import parser
from artbot_scraper.items import EventItem


class NationalArtSchoolSpider(Spider):
    name            = 'National Art School'
    allowed_domains = ['nas.edu.au']
    start_urls      = ['http://www.nas.edu.au/NASGallery/Current-Exhibition-and-Events']

    def parse(self, response):
        for detail in response.xpath('//div[contains(@class, "detail") and not(contains(*/h2, "Contacts & Opening Hours")) and not(contains(*/h2,"Current Exhibition and Events "))]'):
            item = EventItem()
            item['url']         = response.url
            item['venue']       = self.name
            item['title']       = detail.xpath('.//h2/text()').extract_first().strip()
            item['description'] = ''.join(detail.xpath('.//p[img]//following-sibling::*//text()').extract()).strip()
            item['image']       = 'http://www.nas.edu.au/' + detail.xpath('.//img/@src').extract_first()

            season = detail.xpath('.//span//text()').extract_first()

            match  = re.search(u'(?P<start>\d+\s+\w+)[\s\-\–]*(?P<end>\d+\s+\w+\s+\d+)', unicode(season), re.UNICODE)

            if (match):
                start = parser.parse(match.group('start'))
                end   = parser.parse(match.group('end'))

                item['start'] = start
                item['end']   = end

            yield item
