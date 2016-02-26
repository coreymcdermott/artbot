# -*- coding: utf-8 -*-
import re
from dateutil              import parser
from scrapy.spiders        import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from artbot_scraper.items  import EventItem
from pytz                  import timezone


class MildMannersSpider(CrawlSpider):
    name            = 'Mild Manners'
    allowed_domains = ['mild-manners.com']
    start_urls      = ['http://mild-manners.com/']
    rules           = (Rule(LinkExtractor(deny=('ABOUT', 'CONTACT')), callback='parse_exhibition'),)

    def parse_exhibition(self, response):
        item                = EventItem()
        item['url']         = response.url
        item['venue']       = self.name
        item['title']       = ''.join(response.xpath('.//div[contains(@class, "project_content")]//b//text()').extract()).strip()
        item['description'] = ''.join(response.xpath('.//div[contains(@class, "project_content")]//img//following::text()').extract()).strip()
        item['image']       = response.xpath('.//div[contains(@class, "project_content")]//img/@src').extract_first()

        season = response.xpath('.//div[contains(@class, "project_content")]//b/following-sibling::text()[2]').extract_first()
        match  = re.search(u'(?P<start>\w+\s+\d+)[\s\-\–]*(?P<end>\d+)$', season, re.UNICODE)

        if (match):
            tz            = timezone('Australia/Sydney')
            item['start'] = tz.localize(parser.parse(match.group('start')))
            item['end']   = item['start'].replace(day = int(match.group('end')))

        yield item
