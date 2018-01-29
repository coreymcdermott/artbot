# -*- coding: utf-8 -*-
import re
from scrapy               import Spider, Request
from dateutil             import parser
from artbot_scraper.items import EventItem
from pytz                 import timezone


class MinervaSpider(Spider):
    name            = 'Minerva'
    allowed_domains = ['minervasydney.com']
    start_urls      = ['http://www.minervasydney.com/']

    def parse(self, response):
        for href in response.xpath('//section[contains(@class, "currentExhibition")]//a[contains(@class, "exhibitionInformation")]/@href'):
            url = response.urljoin(href.extract())

            yield Request(url, callback=self.parse_current_exhibition)

    def parse_current_exhibition(self, response):
        item                = EventItem()
        item['url']         = response.url
        item['venue']       = self.name
        item['title']       = response.xpath('.//span[contains(@class, "artist")]//text()').extract_first().strip() \
                            + ' - ' \
                            + response.xpath('.//span[contains(@class, "title")]//text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('.//div[contains(@class, "pressRelease")]//text()').extract()).strip()
        item['image']       = response.urljoin(response.xpath('.//div[contains(@class, "documentation")]//img/@src').extract_first())

        season = ' '.join(response.xpath('.//span[contains(@class, "dates")]//text()').extract()).strip()
        match  = re.search(u'(?P<start>\d+\s+\w+)[\s\-\–\—]+(?P<end>\d+\s+\w+,\s+\d+)', season)

        if (match):
            tz             = timezone('Australia/Sydney')
            item['start']  = tz.localize(parser.parse(match.group('start')))
            item['end']    = tz.localize(parser.parse(match.group('end')))

        yield item
