# -*- coding: utf-8 -*-
from dateutil              import parser
from scrapy.spiders        import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from artbot_scraper.items  import EventItem
from pytz                  import timezone


class UNSWGalleriesSpider(CrawlSpider):
    name            = 'UNSW Galleries'
    allowed_domains = ['artdesign.unsw.edu.au']
    start_urls      = ['https://www.artdesign.unsw.edu.au/unsw-galleries']
    rules           = (Rule(LinkExtractor(allow=('unsw-galleries/.+'), deny=('first-fridays', 'community-and-supporters', 'generation-next')), callback='parse_exhibition'),)

    def parse_exhibition(self, response):
        item                = EventItem()
        item['url']         = response.url
        item['venue']       = self.name
        item['title']       = response.xpath('.//h2[contains(@class, "title")]//text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('.//div[contains(@class, "field-type-text-with-summary")]//text()').extract()).strip()
        item['image']       = response.xpath('.//img[contains(@typeof, "foaf:Image")]/@src').extract_first()
        tz                  = timezone('Australia/Sydney')
        item['start']       = tz.localize(parser.parse(response.xpath('.//span[contains(@class, "date-display-start")]/@content').extract_first(), ignoretz=True))
        item['end']         = tz.localize(parser.parse(response.xpath('.//span[contains(@class, "date-display-end")]/@content').extract_first(), ignoretz=True))

        yield item
