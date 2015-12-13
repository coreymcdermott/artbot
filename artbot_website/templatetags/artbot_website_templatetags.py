# -*- coding: utf-8 -*-
import datetime
from   django                  import template
from   django.utils.dateformat import format

register = template.Library()

@register.filter
def conditional_date(date):
    now = datetime.datetime.now()
    if date.year == now.year:
        return format(date, 'j M')
    else:
        return format(date, 'j M, Y')
