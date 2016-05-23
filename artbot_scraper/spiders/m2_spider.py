# -*- coding: utf-8 -*-
import re
from scrapy               import Spider, Request
from dateutil             import parser
from artbot_scraper.items import EventItem
from pytz                 import timezone


class M2Spider(Spider):
    name            = 'm2 Gallery'
    allowed_domains = ['m2gallery.com.au']
    start_urls      = ['http://m2gallery.com.au/Exhibitions.aspx']

    def parse(self, response):
        for href in response.xpath('//div[contains(@id, "dnn_ctr430_ExbList_pnlList")]//ul//li//a/@href'):
            url = response.urljoin(href.extract())

            request = Request(url, callback=self.parse_exhibition)
            request.meta['dont_redirect'] = True
            yield request

    def parse_exhibition(self, response):
        item                = EventItem()
        item['url']         = response.url
        item['venue']       = self.name
        item['title']       = response.xpath('.//div[contains(@class, "m2title")]//text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('.//div[contains(@class, "detailscontent")]//text()').extract()).strip()
        item['image']       = response.urljoin(response.xpath('.//div[contains(@class, "m2rightcolumn")]//img[1]/@src').extract_first())

        season = ''.join(response.xpath('.//div[contains(@class, "showdate")]//text()').extract()).strip()
        match  = re.search(u'(?P<start>\d+\s+\w+\s+\d+).*\s+(?P<end>\d+\s+\w+\s+\d+)', season, re.UNICODE)

        if (match):
            tz            = timezone('Australia/Sydney')
            item['start'] = tz.localize(parser.parse(match.group('start')))
            item['end']   = tz.localize(parser.parse(match.group('end')))

        yield item
