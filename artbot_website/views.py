from django.shortcuts import render
from datetime         import date, datetime, timedelta
from .models          import Event
from pytz             import timezone


def index(request):
    now = datetime.now(timezone('Australia/Sydney')).date()
    if now.isoweekday() in [5, 6, 7]:
        weekend_start = now
    else:
        weekend_start = now + timedelta((5 - now.isoweekday()) % 7)

    events = Event.objects.filter(start__lte = weekend_start, end__gte = weekend_start, published = True).order_by('-start')
    return render(request, 'index.html', {'events': events})
