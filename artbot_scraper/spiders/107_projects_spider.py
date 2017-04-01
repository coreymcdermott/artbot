# -*- coding: utf-8 -*-
import re
from dateutil              import parser
from scrapy.spiders        import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from artbot_scraper.items  import EventItem
from pytz                  import timezone


class OneZeroSevenProjectsSpider(CrawlSpider):
    name            = '107 Projects'
    allowed_domains = ['107.org.au']
    start_urls      = ['http://107.org.au/whats-on/?type=exhibition']
    rules           = (Rule(LinkExtractor(allow=('event/.+'),), callback='parse_exhibition'),)

    def parse_exhibition(self, response):
        item                = EventItem()
        item['url']         = response.url
        item['venue']       = self.name
        item['title']       = response.xpath('//h1//text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('//div[contains(@class, "event-description")]//text()').extract()).strip()
        item['image']       = response.xpath('//section[contains(@class, "article-content")]//img/@src').extract_first()

        season = response.xpath('//strong[contains(text(),"WHEN:")]//following-sibling::text()').extract_first().strip()
        match  = re.match(u'(?P<start>[\d\s\w]+)\s–\s(?P<end>[\d\s\w]+)', season)

        if (match):
            tz            = timezone('Australia/Sydney')
            item['start'] = tz.localize(parser.parse(match.group('start')))
            item['end']   = tz.localize(parser.parse(match.group('end')))

        yield item
