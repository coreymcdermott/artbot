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

    def __init__(self):
        self.download_delay = 3

    def parse(self, response):
        for href in response.xpath('//div[contains(@id, "dnn_ctr430_ExbList_pnlList")]//ul//li//a/@href'):
            url = response.urljoin(href.extract())
            list_id = None

            match = re.search('(?<=listid/)(?P<list_id>\d+)', url)

            if (match):
                list_id = int(match.group('list_id'))

            # Only scrape post 2018 exhibitions.
            if (list_id >= 178):
                request = Request(url, callback=self.parse_exhibition)
                request.meta['dont_redirect'] = True
                yield request
            else:
                continue

    def parse_exhibition(self, response):
        response = response.replace(body=response.body.replace(b'<br>', b'\n'))

        item                = EventItem()
        item['url']         = response.url
        item['venue']       = self.name
        item['title']       = response.xpath('.//div[contains(@class, "m2title")]//text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('.//div[contains(@class, "detailscontent")]//text()').extract()).strip()
        item['image']       = response.urljoin(response.xpath('.//div[contains(@class, "m2rightcolumn")]//img[1]/@src').extract_first())

        season = ''.join(response.xpath('.//div[contains(@class, "showdate")]//text()').extract()).strip()
        match  = re.search(u'(?P<start>\d+\s+\w+\s+\d+).*\s+(?P<end>\d+\s+\w+\s+\d+)', season)

        if (match):
            tz            = timezone('Australia/Sydney')
            item['start'] = tz.localize(parser.parse(match.group('start')))
            item['end']   = tz.localize(parser.parse(match.group('end')))


        yield item
