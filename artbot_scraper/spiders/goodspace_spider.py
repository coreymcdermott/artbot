# -*- coding: utf-8 -*-
import re
from scrapy               import Spider, Request
from dateutil             import parser
from artbot_scraper.items import EventItem
from pytz                 import timezone


class AmbushSpider(Spider):
    name            = "Goodspace"
    allowed_domains = ["goodspace.co"]
    start_urls      = ["http://goodspace.co/upcoming/"]

    def parse(self, response):
        for href in response.xpath('//a[contains(@class, "project")]/@href'):
            url = response.urljoin(href.extract())

            yield Request(url, callback=self.parse_event)

    def parse_event(self, response):
        item                = EventItem()
        item['url']         = response.url
        item['venue']       = self.name
        item['title']       = response.xpath('//h1/text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('//div[contains(@class, "event_details")]//text()').extract())
        item['image']       = response.xpath('//figure[contains(@class, "amb_gal_img")]//img/@src').extract_first()

        time  = ''.join(response.xpath('//time//text()').extract())
        match = re.match('(?P<start>[a-zA-Z]+\d+)(?P<end>[a-zA-Z]+\d+)', time)

        if (match):
            tz            = timezone('Australia/Sydney')
            item['start'] = tz.localize(parser.parse(match.group('start')))
            item['end']   =  tz.localize(parser.parse(match.group('end')))

        yield item
