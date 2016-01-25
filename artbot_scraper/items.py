# -*- coding: utf-8 -*-
from scrapy_djangoitem     import DjangoItem
from artbot_website.models import Event


class EventItem(DjangoItem):
    django_model = Event
