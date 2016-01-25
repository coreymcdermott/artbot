# -*- coding: utf-8 -*-
import re
from scrapy               import Spider, Request
from dateutil             import parser
from artbot_scraper.items import EventItem


class UTSSpider(Spider):
    name            = 'UTS'
    allowed_domains = ['art.uts.edu.au']
    start_urls      = ['http://art.uts.edu.au/index.php/exhibitions/']

    def parse(self, response):
        for href in response.xpath('//a[contains(@class, "listed-item-link")]/@href'):
            url = response.urljoin(href.extract())

            yield Request(url, callback=self.parse_exhibition)

    def parse_exhibition(self, response):
        item = EventItem()
        item['url']         = response.url
        item['venue']       = 'UTS ART'
        item['title']       = response.xpath('//h1[contains(@class, "entry-title")]/text()').extract_first().strip() \
                            + ' - ' \
                            + response.xpath('//h2[contains(@class, "entry-subtitle")]/text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('//div[contains(@class, "entry-content")]//text()').extract()).strip()
        item['image']       = response.xpath('//img[contains(@class, "large-crop")]/@src').extract_first()
        item['start']       = parser.parse(response.xpath('//span[contains(@class, "start-date")]/text()').extract_first().strip(), fuzzy = True)
        item['end']         = parser.parse(response.xpath('//span[contains(@class, "end-date")]/text()').extract_first().strip(), fuzzy = True)

        yield item
