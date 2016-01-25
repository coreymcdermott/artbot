# -*- coding: utf-8 -*-
import re
from scrapy               import Spider, Request
from dateutil             import parser
from artbot_scraper.items import EventItem


class AmbushSpider(Spider):
    name            = "Goodspace"
    allowed_domains = ["goodspace.co"]
    start_urls      = ["http://goodspace.co/upcoming/"]
    base_url        = "http://goodspace.co/upcoming/"

    def parse(self, response):
        for href in response.xpath('//a[contains(@class, "project")]/@href'):
            url = response.urljoin(base_url, href.extract())

            yield Request(url, callback=self.parse_event)

    def parse_event(self, response):
        item = EventItem()
        item['url']         = response.url
        item['venue']       = "Goodspace"
        item['title']       = response.xpath('//h1/text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('//div[contains(@class, "event_details")]//text()').extract())
        item['image']       = response.xpath('//figure[contains(@class, "amb_gal_img")]//img/@src').extract_first()

        time = ''.join(response.xpath('//time//text()').extract())
        match   = re.match('(?P<start>[a-zA-Z]+\d+)(?P<end>[a-zA-Z]+\d+)', time)

        if (match):
            start = parser.parse(match.group('start'))
            end   = parser.parse(match.group('end'))

            item['start']  = start
            item['end']    = end

        yield item
