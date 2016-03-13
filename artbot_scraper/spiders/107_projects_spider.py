# -*- coding: utf-8 -*-
import re
from dateutil              import parser
from scrapy.spiders        import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from artbot_scraper.items  import EventItem
from pytz                  import timezone


class OneZeroSevenProjectsSpider(CrawlSpider):
    name            = '107 Projects'
    allowed_domains = ['107projects.org']
    start_urls      = ['http://107projects.org/whats-on/?type=exhibition']
    rules           = (Rule(LinkExtractor(allow=('event/.+'),), callback='parse_exhibition'),)

    def parse_exhibition(self, response):
        item                = EventItem()
        item['url']         = response.url
        item['venue']       = self.name
        item['title']       = response.xpath('//h1//text()').extract_first().strip()
        item['description'] = ''.join(response.xpath('//b[contains(text(),"COST:")]//parent::h4/following-sibling::p[1]/text()').extract()).strip()
        item['image']       = response.xpath('//section[contains(@class, "article-content")]//img/@src').extract_first()

        season = response.xpath('//b[contains(text(),"WHEN:")]//parent::h4/text()').extract_first().strip()
        match  = re.match('[\w+\s]*(?P<start>\d+\s+\w+\s+\d+)[\s\-]*(?P<end>\d+\s+\w+\s+\d+)', season)

        if (match):
            tz            = timezone('Australia/Sydney')
            item['start'] = tz.localize(parser.parse(match.group('start')))
            item['end']   = tz.localize(parser.parse(match.group('end')))

        yield item
