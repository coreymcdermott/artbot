from django.contrib       import admin
from django.contrib.admin import SimpleListFilter
from datetime             import date, datetime, timedelta
from .models              import Event

class EventWeekendFilter(SimpleListFilter):
    title = ('weekend')
    parameter_name = 'weekend'

    def lookups(self, request, model_admin):
        return (
            ('THIS_WEEKEND', ('This weekend')),
            ('NEXT_WEEKEND', ('Next weekend')),
        )

    def queryset(self, request, queryset):

        this_weekend = date.today() + timedelta((6 - date.today().isoweekday()) % 7 )
        next_weekend = this_weekend + timedelta(days = 7)

        if self.value() == 'THIS_WEEKEND':
            return queryset.filter(start__lte = this_weekend, end__gte = this_weekend)
        elif self.value() == 'NEXT_WEEKEND':
            return queryset.filter(start__lte = next_weekend, end__gte = next_weekend)

def publish(modeladmin, request, queryset):
    queryset.update(published = True)
publish.short_description = "Publish selected events"

def withdraw(modeladmin, request, queryset):
    queryset.update(published = False)
withdraw.short_description = "Withdraw selected events"

class EventAdmin(admin.ModelAdmin):
    list_filter   = ('published', EventWeekendFilter,)
    list_display  = ('title', 'venue', 'start', 'end', 'created', 'published')
    search_fields = ('title', 'venue')
    actions       = [publish, withdraw,]

admin.site.register(Event, EventAdmin)
