# -*- coding: utf-8 -*-
import re
from dateutil              import parser
from scrapy.spiders        import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from artbot_scraper.items  import EventItem
from pytz                  import timezone


class PompomSpider(CrawlSpider):
    name            = 'Galerie pompom'
    allowed_domains = ['galeriepompom.com']
    start_urls      = ['http://galeriepompom.com/galerie-pompom--exhibitions.html']
    rules           = (Rule(LinkExtractor(deny=('exhibitions-2016', ), allow=('2016', )), callback='parse_exhibition'),)

    def parse_exhibition(self, response):
        item          = EventItem()
        item['url']   = response.url
        item['venue'] = self.name
        item['title'] = response.xpath('//div[contains(@data-muse-type, "txt_frame")]/p[2]/text()').extract_first().strip()
        item['image'] = response.urljoin(response.xpath('//div[contains(@class, "SlideShowWidget")]//img/@data-src').extract_first())

        season = response.xpath('//div[contains(@data-muse-type, "txt_frame")]/p[1]/text()').extract_first().strip()
        match  = re.match('(?P<start>[\d+\s+\w+]*)[\s\-]*(?P<end>\d+\s+\w+\s+\d+)', season)

        if (match):
            tz = timezone('Australia/Sydney')

            if len(match.group('start')) <= 2:
                item['end']   = tz.localize(parser.parse(match.group('end')))
                item['start'] = item['end'].replace(day = int(match.group('start')))
            else:
                item['start'] = tz.localize(parser.parse(match.group('start')))
                item['end']   = tz.localize(parser.parse(match.group('end')))

        yield item
