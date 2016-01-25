# -*- coding: utf-8 -*-
import re
from scrapy               import Spider, Request
from dateutil             import parser
from artbot_scraper.items import EventItem


class FirstdraftSpider(Spider):
    name            = 'Firstdraft'
    allowed_domains = ['firstdraft.org.au']
    start_urls      = ['http://firstdraft.org.au/exhibitions/']

    def parse(self, response):
        for href in response.xpath('//article//a/@href'):
            url = response.urljoin(href.extract())

            yield Request(url, callback=self.parse_exhibition)

    def parse_exhibition(self, response):
        item = EventItem()
        item['url']         = response.url
        item['venue']       = 'Firstdraft'
        item['title']       = response.xpath('//div[contains(concat(" ", @class, " "), " exhibition ")]/h1/text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('//div[contains(concat(" ", @class, " "), " exhibition ")]//h3//text()').extract()).strip()
        item['image']       = response.xpath('//section[contains(concat(" ", @class, " "), " images_container ")]//img/@src').extract_first()

        season  = response.xpath('//div[contains(concat(" ", @class, " "), " secondary ")]//p[contains(@class, "dateX")]//text()').extract_first().strip()
        match   = re.match(u'(?P<start>\d+\.\d+\.\d+)[\s\-\–]*(?P<end>\d+\.\d+\.\d+)', season, re.UNICODE)

        if (match):
            item['start'] = parser.parse(match.group('start'), dayfirst = True)
            item['end']   = parser.parse(match.group('end'),   dayfirst = True)

        yield item
