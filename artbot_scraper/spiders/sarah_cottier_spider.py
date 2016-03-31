# -*- coding: utf-8 -*-
import re
from dateutil              import parser
from scrapy.spiders        import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from artbot_scraper.items  import EventItem
from pytz                  import timezone


class SarahCottierGallery(CrawlSpider):
    name            = 'Sarah Cottier Gallery'
    allowed_domains = ['sarahcottiergallery.com']
    start_urls      = ['http://www.sarahcottiergallery.com/']
    rules           = (Rule(LinkExtractor(allow=('exhibition/.+', )), callback='parse_exhibition'),)

    def parse_exhibition(self, response):
        item          = EventItem()
        item['url']   = response.url
        item['venue'] = self.name
        item['image'] = None

        # If JavaScript is exectued, image could be extracted with
        # response.xpath('//span[contains(@id, "media_holder")]/img/@src').extract_first()

        alt   = response.xpath('//a[contains(@href,"' + response.url + '")]/img/@alt').extract_first()
        match = re.search('(?P<title>[\w+\s+]*)(?P<start>\d+[\s+\w+]*)[\s\-]*(?P<end>\d+\s+\w+,\s+\d+)', alt)

        if (match):
            tz            = timezone('Australia/Sydney')
            item['end']   = tz.localize(parser.parse(match.group('end')))
            item['start'] = tz.localize(parser.parse(match.group('start')))
            item['title'] = match.group('title').strip()

        yield item