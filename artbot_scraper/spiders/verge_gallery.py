# -*- coding: utf-8 -*-
import re
from dateutil              import parser
from scrapy.spiders        import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from artbot_scraper.items  import EventItem
from pytz                  import timezone

class VergeGallerySpider(CrawlSpider):
    name            = 'Verge Gallery'
    allowed_domains = ['verge-gallery.net']
    start_urls      = ['https://verge-gallery.net/category/current/']
    rules           = (Rule(LinkExtractor(allow=('/\d+\/\d+\/\d+'), deny=('eoi')), callback='parse_exhibition'),)

    def parse_exhibition(self, response):
        item_one = EventItem()
        item_two = EventItem()

        season   = response.xpath('//p[contains(@style, "outline: none;")]/text()').extract_first()

        if season is not None:
            match = re.search('(?P<start>(?<=OPENING\s)\w+\s+\d+).*(?P<end>(?<=CONTINUING TO\s)\w+\s+\d+)', season, re.MULTILINE)

            if (match):
                tz = timezone('Australia/Sydney')
                item_one['start'] = tz.localize(parser.parse(match.group('start')))
                item_one['end']   = tz.localize(parser.parse(match.group('end')))
                item_two['start'] = tz.localize(parser.parse(match.group('start')))
                item_two['end']   = tz.localize(parser.parse(match.group('end')))

        item_one['url']         = response.url
        item_one['venue']       = self.name
        item_one['title']       = response.xpath('//hr//following-sibling::p[1]/text()').extract()[0].strip()
        item_one['description'] = response.xpath('//hr//following-sibling::p[1]/following-sibling::p[1]/text()').extract()[0].strip()
        item_one['image']       = response.xpath('//hr//following-sibling::p[1]/following-sibling::div[1]//img/@src').extract()[0].strip()

        yield item_one

        item_two['url']         = response.url
        item_two['venue']       = self.name
        item_two['title']       = response.xpath('//hr//following-sibling::p[1]/text()').extract()[1].strip()
        item_two['description'] = response.xpath('//hr//following-sibling::p[1]/following-sibling::p[1]/text()').extract()[1].strip()
        item_two['image']       = response.xpath('//hr//following-sibling::p[1]/following-sibling::div[1]//img/@src').extract()[1].strip()

        yield item_two
