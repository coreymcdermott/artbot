#-*- coding: utf-8 -*-
import re
from scrapy               import Spider, Request
from dateutil             import parser
from artbot_scraper.items import EventItem

class ArthouseSpider(Spider):
    name            = 'Arthouse'
    allowed_domains = ['www.arthousegallery.com.au']
    start_urls      = ['http://www.arthousegallery.com.au/exhibitions/']

    def parse(self, response):
        for href in response.xpath('//div[contains(@id, "index")]//li//a/@href'):
            url = response.urljoin(href.extract())

            yield Request(url, callback=self.parse_exhibition)

    def parse_exhibition(self, response):
        item = EventItem()
        item['url']         = response.url
        item['venue']       = 'Arthouse Gallery'
        item['title']       = response.xpath('//div[contains(@id, "headerTitle")]//text()').extract_first().strip() \
                            + ' - ' \
                            + response.xpath('//div[contains(@id, "headerSubTitle")]//em/text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('//div[contains(@id, "exhibition")]//hr/following-sibling::p//text()').extract()).strip()
        item['image']       = 'http://www.arthousegallery.com.au/' + response.xpath('//img//@src').extract_first()

        season  = ''.join(map(unicode, response.xpath('//div[contains(@id, "headerSubTitle")]//text()[not(ancestor::em)]').extract())).strip()
        match   = re.match(u'(?P<start>^[\d\w\s]+)[\s\-\–]*(?P<end>[\d\w\s]+$)', season, re.UNICODE)

        if (match):
            start = parser.parse(match.group('start'), fuzzy = True)
            end   = parser.parse(match.group('end'), fuzzy = True)

            if (re.match(u'^\d+$', match.group('start'), re.UNICODE)):
                start = start.replace(month=end.month, year=end.year)

            if (re.match(u'^\d+\s+\w+$', match.group('start'), re.UNICODE)):
                start = start.replace(year=end.year)

            item['start'] = start
            item['end']   = end

        yield item
