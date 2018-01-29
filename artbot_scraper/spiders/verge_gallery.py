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
    rules           = (Rule(LinkExtractor(allow=('/\d+\/\d+\/\d+'), deny=('eoi', '2017-program')), callback='parse_exhibition'),)

    def parse_exhibition(self, response):
        item                = EventItem()
        item['url']         = response.url
        item['venue']       = self.name
        item['title']       = response.xpath('//h2[contains(@class, "entry-title")]/text()').extract_first().strip()
        item['description'] = response.xpath('//hr//following-sibling::p[1]//text()').extract_first().strip()
        item['image']       = response.xpath('//figure[contains(@class, "featured-image")]//img/@src').extract_first().strip()

        season = response.xpath('//h2[contains(@class, "entry-title")]/text()').extract_first()
        match  = re.search('(?P<start>(?<=\:\:\s)\w+\s+\d+)[\s\-\–]*(?P<end>\w+\s+\d+)', season)

        if (match):
            tz = timezone('Australia/Sydney')
            item['start'] = tz.localize(parser.parse(match.group('start')))
            item['end']   = tz.localize(parser.parse(match.group('end')))

        yield item
