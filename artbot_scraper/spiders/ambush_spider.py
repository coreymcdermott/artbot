#-*- coding: utf-8 -*-
import re
from scrapy               import Spider, Request
from dateutil             import parser, relativedelta
from artbot_scraper.items import EventItem

class AmbushSpider(Spider):
    name            = "aMBUSH"
    allowed_domains = ["ambushgallery.com"]
    start_urls      = ["http://ambushgallery.com/events/"]

    def parse(self, response):
        for href in response.xpath('//a[contains(@class, "upcoming_info_inner")]/@href'):
            url = response.urljoin(href.extract())

            yield Request(url, callback=self.parse_event)

    def parse_event(self, response):
        item = EventItem()
        item['url']         = response.url
        item['venue']       = "aMBUSH"
        item['title']       = response.xpath('//h1/text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('//div[contains(@class, "event_details")]//text()').extract())
        item['image']       = response.xpath('//figure[contains(@class, "amb_gal_img")]//img/@src').extract_first()

        time = ''.join(response.xpath('//time//text()').extract())
        match   = re.match('(?P<start>[a-zA-Z]+\d+)(?P<end>[a-zA-Z]+\d+)', time)

        if (match):
            start = parser.parse(match.group('start'))
            end   = parser.parse(match.group('end'))

            if (end < start):
                end = end + relativedelta.relativedelta(years=+1)

            item['start']  = start
            item['end']    = end

        yield item
