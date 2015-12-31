from django.contrib       import admin, messages
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

        if date.today().isoweekday() in [5,6,7]:
            this_weekend_start = date.today()
        else:
            this_weekend_start = date.today() + timedelta((5 - date.today().isoweekday()) % 7 )

        if date.today().isoweekday() == 5:
            next_weekend_start = date.today() + timedelta(days = 7)
        else:
            next_weekend_start = date.today() + timedelta((5 - date.today().isoweekday()) % 7 ) + timedelta(days = 7)

        if self.value() == 'THIS_WEEKEND':
            return queryset.filter(start__lte = this_weekend_start, end__gte = this_weekend_start)
        elif self.value() == 'NEXT_WEEKEND':
            return queryset.filter(start__lte = next_weekend_start, end__gte = next_weekend_start)

def publish(modeladmin, request, queryset):
    queryset.update(published = True)
publish.short_description = "Publish"

def withdraw(modeladmin, request, queryset):
    queryset.update(published = False)
withdraw.short_description = "Withdraw"

def crop_image(modeladmin, request, queryset):
    for event in queryset:
        try:
            print event
            event.crop_image()
        except Exception as e:
            messages.error(request, str(e))
crop_image.short_description = "Crop and transload images"

class EventAdmin(admin.ModelAdmin):
    list_filter   = ('published', EventWeekendFilter,)
    list_display  = ('title', 'venue', 'start', 'end', 'created', 'published')
    search_fields = ('title', 'venue')
    actions       = [publish, withdraw, crop_image]

admin.site.register(Event, EventAdmin)
