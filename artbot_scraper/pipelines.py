# -*- coding: utf-8 -*-
from django.db         import IntegrityError
from scrapy.exceptions import DropItem
from titlecase         import titlecase
from dateutil          import parser, relativedelta


class EventPipeline(object):
    def process_item(self, item, spider):
        item['title_raw'] = item['title']
        item['title']    = titlecase(item['title'])

        if 'end' in item and 'start' in item:
            if (item['end'] < item['start']):
                item['end'] = item['end'] + relativedelta.relativedelta(years =+ 1)

        try:
            item.save()
        except IntegrityError:
            raise DropItem('Duplicate: ' + item['venue'] + ' - ' + item['title'])
        return item
