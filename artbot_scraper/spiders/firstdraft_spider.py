# -*- coding: utf-8 -*-
import re
from scrapy               import Spider, Request
from dateutil             import parser
from artbot_scraper.items import EventItem
from pytz                 import timezone


class FirstdraftSpider(Spider):
    name            = 'Firstdraft'
    allowed_domains = ['firstdraft.org.au']
    start_urls      = ['https://firstdraft.org.au/exhibition']

    def parse(self, response):
        for href in response.xpath('//div[contains(@class, "summary-title")]//a/@href'):
            url = response.urljoin(href.extract())

            yield Request(url, callback=self.parse_exhibition)

    def parse_exhibition(self, response):
        item                = EventItem()
        item['url']         = response.url
        item['venue']       = self.name
        item['title']       = response.xpath('//div[contains(@data-layout-label, "Post Body")]//h1/text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('//div[contains(@data-layout-label, "Post Body")]//p/text()').extract()).strip()
        item['image']       = response.xpath('//div[contains(@data-layout-label, "Post Body")]//img/@src').extract_first()

        event_dates = response.xpath('//time[contains(@class, "event-date")]//@datetime').extract()
        tz = timezone('Australia/Sydney')
        item['start'] = tz.localize(parser.parse(event_dates[0], dayfirst = True))
        item['end'] = tz.localize(parser.parse(event_dates[1], dayfirst = True))

        yield item
