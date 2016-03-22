# -*- coding: utf-8 -*-
import re
from scrapy               import Spider, Request
from dateutil             import parser
from artbot_scraper.items import EventItem
from pytz                 import timezone


class AGNSpider(Spider):
    name            = 'AGN'
    allowed_domains = ['artgallery.nsw.gov.au']
    start_urls      = ['http://www.artgallery.nsw.gov.au/exhibitions/current/']

    def parse(self, response):
        for href in response.xpath('//div[contains(@class, "currentExhibition")]//a[1]/@href'):
            url = response.urljoin(href.extract())
            if 'brett-whiteley-studio' in url:
                continue

            yield Request(url, callback=self.parse_current_exhibition)

    def parse_current_exhibition(self, response):
        item                = EventItem()
        item['url']         = response.url
        item['venue']       = self.name
        item['title']       = response.xpath('.//h2//text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('.//div[contains(@class, "lumpy-main")]//text()').extract()).strip()
        item['image']       = response.urljoin(response.xpath('.//div[contains(@id, "content")]//img/@src').extract_first())

        season = ' '.join(response.xpath('.//div[contains(@class, "exhib-details")]//h3/text()').extract()).strip()
        match  = re.search(u'(?P<start>\d+\s+\w+[\s+\d]*)[\s\-\–]*(?P<end>\d+\s+\w+\s+\d+)$', season, re.UNICODE)

        if (match):
            tz             = timezone('Australia/Sydney')
            item['start']  = tz.localize(parser.parse(match.group('start')))
            item['end']    = tz.localize(parser.parse(match.group('end')))

        yield item
