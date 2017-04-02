# -*- coding: utf-8 -*-
import re
from scrapy               import Spider, Request
from dateutil             import parser
from artbot_scraper.items import EventItem
from pytz                 import timezone


class MaySpaceSpider(Spider):
    name            = 'May Space'
    allowed_domains = ['mayspace.com.au']
    start_urls      = ['http://www.mayspace.com.au/ex_view.php?ex_typeID=1']

    def parse(self, response):
        for href in response.xpath('//div[contains(@class, "ex-right")]//a/@href'):
            url = response.urljoin(href.extract())

            yield Request(url, callback=self.parse_current_exhibition)

    def parse_current_exhibition(self, response):
        item                = EventItem()
        item['url']         = response.url
        item['venue']       = self.name
        item['title']       = response.xpath('.//div[contains(@class, "side2")]//h2//text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('.//p[contains(@id, "printcat")]/following-sibling::p//text()').extract()).strip()
        item['image']       = response.urljoin(response.xpath('.//div[contains(@class, "artist-grid-image2")]//img/@src').extract_first())

        season = ' '.join(response.xpath('.//div[contains(@class, "side2")]/h2/following-sibling::p[1]/strong/text()').extract()).strip()
        match  = re.search(u'(?P<start>\d+\s+\w+)\sto\s(?P<end>\d+\s+\w+\s+\d+)', season, re.UNICODE)

        if (match):
            tz             = timezone('Australia/Sydney')
            item['start']  = tz.localize(parser.parse(match.group('start')))
            item['end']    = tz.localize(parser.parse(match.group('end')))

        yield item
