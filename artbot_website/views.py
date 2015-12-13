from django.shortcuts import render
from datetime         import date, datetime, timedelta
from .models          import Event

def index(request):
    if date.today().isoweekday() in [5,6,7]:
        weekend_start = date.today()
    else:
        weekend_start = date.today() + timedelta((5 - date.today().isoweekday()) % 7 )

    events = Event.objects.filter(start__lte = weekend_start, end__gte = weekend_start).order_by('-start')
    return render(request, 'index.html', {'events': events})
