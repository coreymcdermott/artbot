# -*- coding: utf-8 -*-
import re
from scrapy               import Spider, Request
from dateutil             import parser
from artbot_scraper.items import EventItem
from pytz                 import timezone


class TheCommercialSpider(Spider):
    name            = 'The Commercial'
    allowed_domains = ['thecommercialgallery.com']
    start_urls      = ['http://thecommercialgallery.com/program']

    def parse(self, response):
        for href in response.xpath('//a[contains(@class, "site1_program-list-item")]'):
            item = EventItem()
            url  = response.urljoin(href.xpath('@href').extract_first())

            item['url']   = url
            item['venue'] = self.name

            text  = href.xpath('text()').extract_first().strip()
            match = re.search(u'(?P<start>\d+\/\d+\/\d+)[\s\-\–]*(?P<end>\d+\/\d+\/\d+)\:(?P<title>.*)', text, re.UNICODE)

            if (match):
                tz    = timezone('Australia/Sydney')
                item['start'] = tz.localize(parser.parse(match.group('start'), dayfirst = True))
                item['end']   = tz.localize(parser.parse(match.group('end'), dayfirst = True))
                item['title'] = match.group('title').strip()

            yield Request(url, callback=self.parse_exhibition, meta={'item': item})

    def parse_exhibition(self, response):
        item = response.meta['item']
        url  = response.urljoin(response.xpath('//div[contains(@id, "collection-container")]//a/@href').extract_first())

        yield Request(url, callback=self.parse_artwork, meta={'item': item})

    def parse_artwork(self, response):
        item = response.meta['item']

        item['image'] = response.urljoin(response.xpath('//div[contains(@class, "artwork-main-view ")]//img/@src').extract_first())

        yield item
