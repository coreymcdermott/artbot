# -*- coding: utf-8 -*-
import re
from scrapy               import Spider, Request
from dateutil             import parser
from artbot_scraper.items import EventItem
from pytz                 import timezone


class AGNSpider(Spider):
    name            = '4A Centre for Contemporary Asian Art'
    allowed_domains = ['www.4a.com.au']
    start_urls      = ['http://www.4a.com.au/whats-on/']

    def parse(self, response):
        for href in response.xpath('//div[contains(@class, "article")]//a[1]/@href'):
            url = response.urljoin(href.extract())

            yield Request(url, callback=self.parse_article)

    def parse_article(self, response):
        item                = EventItem()
        item['url']         = response.url
        item['venue']       = self.name
        item['title']       = response.xpath('.//h1//text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('.//div[contains(@id, "main")]//p[2]//text()').extract())
        item['image']       = response.urljoin(response.xpath('.//div[contains(@class, "group")]//img/@src').extract_first())

        season = response.xpath('.//div[contains(@id, "main")]//p[1]//text()').extract_first().strip()
        match  = re.search(u'\.\s+(?P<start>[\d+\s+\w]+)[\s\-\–]*(?P<end>[\d+\s+\w]+)\.', season, re.UNICODE)

        if (match):
            tz    = timezone('Australia/Sydney')
            start = tz.localize(parser.parse(match.group('start'), fuzzy = True))
            end   = tz.localize(parser.parse(match.group('end'), fuzzy = True))

            if (re.match(u'^\d+$', match.group('start'), re.UNICODE)):
                start = start.replace(month=end.month, year=end.year)

            if (re.match(u'^\d+\s+\w+$', match.group('start'), re.UNICODE)):
                start = start.replace(year=end.year)

            item['start'] = start
            item['end']   = end

        yield item
