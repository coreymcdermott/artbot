# -*- coding: utf-8 -*-
from django.db         import IntegrityError
from scrapy.exceptions import DropItem

class EventPipeline(object):
    def process_item(self, item, spider):
        try:
            item.save()
        except IntegrityError:
            raise DropItem('Duplicate: ' + item['venue'] + ' - ' + item['title'])
        return item
