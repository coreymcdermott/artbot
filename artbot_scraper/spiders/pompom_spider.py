#-*- coding: utf-8 -*-
import re
from dateutil              import parser, relativedelta
from scrapy.spiders        import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from artbot_scraper.items  import EventItem

class PompomSpider(CrawlSpider):
    name            = 'Pompom'
    allowed_domains = ['galeriepompom.com']
    start_urls      = ['http://galeriepompom.com/galerie-pompom--exhibitions.html']
    rules           = (Rule(LinkExtractor(allow=('2015', )), callback='parse_exhibition'),)

    def parse_exhibition(self, response):
        item = EventItem()
        item['url']         = response.url
        item['venue']       = 'Galerie pompom'
        item['title']       = response.xpath('//div[@class = "position_content"]/div[3]/p[1]/text()').extract_first().strip() + ' - ' +\
                              response.xpath('//div[@class = "position_content"]/div[3]/p[2]/text()').extract_first().strip()
        item['image']       = 'http://galeriepompom.com/' + response.xpath('//div[contains(@class, "SSSlide")]//img/@data-src').extract_first()

        season  = response.xpath('//div[@class = "position_content"]/div[3]/p[4]/text()').extract_first().strip()
        match   = re.match('(?P<start>\d+\s+\w+)[\s\-]*(?P<end>\d+\s+\w+)', season)

        if (match):
            start = parser.parse(match.group('start'))
            end   = parser.parse(match.group('end'))

            if (end < start):
                end = end + relativedelta.relativedelta(years=+1)

            item['start']  = start
            item['end']    = end

        yield item
