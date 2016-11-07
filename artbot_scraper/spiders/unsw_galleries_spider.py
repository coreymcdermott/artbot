# -*- coding: utf-8 -*-
import re
from dateutil              import parser
from scrapy.spiders        import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from artbot_scraper.items  import EventItem
from pytz                  import timezone


class UNSWGalleriesSpider(CrawlSpider):
    name            = 'UNSW Galleries'
    allowed_domains = ['artdesign.unsw.edu.au']
    start_urls      = ['https://www.artdesign.unsw.edu.au/unsw-galleries']
    rules           = (Rule(LinkExtractor(allow=('unsw-galleries/.+'), deny=('first-fridays', 'community-and-supporters', 'generation-next', 'past-exhibitions', 'upcoming-exhibitions', 'about', 'library', 'on-tour')), callback='parse_exhibition'),)

    def parse_exhibition(self, response):
        item                = EventItem()
        item['url']         = response.url
        item['venue']       = self.name
        item['title']       = response.xpath('.//h2[contains(@class, "title")]//text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('.//div[contains(@class, "field-type-text-with-summary")]//text()').extract()).strip()
        item['image']       = response.xpath('.//img[contains(@typeof, "foaf:Image")]/@src').extract_first()

        season = response.xpath('.//span[contains(text(), "When")]/following-sibling::span/text()').extract_first().strip()
        match  = re.search(u'(?P<start>\d+\s+\w+[\s+\d]*)[\s\-\–]*(?P<end>\d+\s+\w+\s+\d+)$', season, re.UNICODE)

        if (match):
            tz             = timezone('Australia/Sydney')
            item['start']  = tz.localize(parser.parse(match.group('start')))
            item['end']    = tz.localize(parser.parse(match.group('end')))

        yield item
