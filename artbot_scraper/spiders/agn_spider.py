#-*- coding: utf-8 -*-
import re
from scrapy               import Spider, Request
from dateutil             import parser, relativedelta
from artbot_scraper.items import EventItem

class AGNSpider(Spider):
    name            = 'AGN'
    allowed_domains = ['artgallery.nsw.gov.au']
    start_urls      = ['http://www.artgallery.nsw.gov.au/exhibitions/current/']

    def parse(self, response):
        for href in response.xpath('//div[contains(@class, "currentExhibition")]//a[1]/@href'):
            url = response.urljoin(href.extract())

            yield Request(url, callback=self.parse_current_exhibition)

    def parse_current_exhibition(self, response):
        item = EventItem()
        item['url']         = response.url
        item['venue']       = 'AGN'
        item['title']       = response.xpath('.//h2//text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('.//div[contains(@class, "lumpy-main")]//text()').extract()).strip()
        item['image']       = 'http://www.artgallery.nsw.gov.au' + response.xpath('.//div[contains(@id, "content")]//img/@src').extract_first()

        season  = ' '.join(response.xpath('.//div[contains(@class, "exhib-details")]//h3/text()').extract()).strip()
        match   = re.search(u'(?P<start>\d+\s+\w+[\s+\d]*)[\s\-\–]*(?P<end>\d+\s+\w+\s+\d+)$', season, re.UNICODE)

        if (match):
            start = parser.parse(match.group('start'))
            end   = parser.parse(match.group('end'))

            if (end < start):
                end = end + relativedelta.relativedelta(years=+1)

            item['start']  = start
            item['end']    = end

        yield item
