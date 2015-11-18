from django.shortcuts import render
from datetime         import date, datetime, timedelta
from .models          import Event

def index(request):
    weekend_start = date.today()  + timedelta((6 - date.today().isoweekday()) % 7 )
    weekend_end   = weekend_start + timedelta(1)
    events = Event.objects.filter(start__lte = weekend_start, end__gte = weekend_end).order_by('-start')
    return render(request, 'index.html', {'events': events})
