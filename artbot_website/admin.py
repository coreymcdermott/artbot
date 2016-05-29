from django.contrib       import admin, messages
from django.contrib.admin import SimpleListFilter
from datetime             import date, datetime, timedelta
from .models              import Event, Log, Sponsor
from pytz                 import timezone


class EventWeekendFilter(SimpleListFilter):
    title = ('weekend')
    parameter_name = 'weekend'

    def lookups(self, request, model_admin):
        return (
            ('THIS_WEEKEND', ('This weekend')),
            ('NEXT_WEEKEND', ('Next weekend')),
        )

    def queryset(self, request, queryset):
        now = datetime.now(timezone('Australia/Sydney')).date()

        if now.isoweekday() in [5, 6, 7]:
            this_weekend_start = now
        else:
            this_weekend_start = now + timedelta((5 - now.isoweekday()) % 7)

        if now.isoweekday() == 5:
            next_weekend_start = now + timedelta(days = 7)
        else:
            next_weekend_start = now + timedelta((5 - now.isoweekday()) % 7) + timedelta(days = 7)

        if self.value() == 'THIS_WEEKEND':
            return queryset.filter(start__lte = this_weekend_start, end__gte = this_weekend_start)
        elif self.value() == 'NEXT_WEEKEND':
            return queryset.filter(start__lte = next_weekend_start, end__gte = next_weekend_start)


class EventStartFilter(SimpleListFilter):
    title = ('start')
    parameter_name = 'start'

    def lookups(self, request, model_admin):
        return (
            ('FUTURE', ('Future')),
            ('PAST', ('Past')),
        )

    def queryset(self, request, queryset):
        today = date.today()

        if self.value() == 'FUTURE':
            return queryset.filter(start__gte = today)
        elif self.value() == 'PAST':
            return queryset.filter(start__lt = today)


def publish(modeladmin, request, queryset):
    queryset.update(status = Event.PUBLISHED_STATUS)
publish.short_description = "Publish"


def withdraw(modeladmin, request, queryset):
    queryset.update(status = Event.DRAFT_STATUS)
withdraw.short_description = "Withdraw"


def hide(modeladmin, request, queryset):
    queryset.update(status = Event.HIDDEN_STATUS)
hide.short_description = "Hide"


def crop_image(modeladmin, request, queryset):
    for event in queryset:
        try:
            print event
            event.crop_image()
        except Exception as e:
            messages.error(request, str(e))
crop_image.short_description = "Crop and transload images"


class EventAdmin(admin.ModelAdmin):
    list_filter   = ('status', EventWeekendFilter, EventStartFilter)
    list_display  = ('title', 'venue', 'start', 'end', 'created', 'status')
    search_fields = ('title', 'venue')
    exclude       = ('titleRaw',)
    actions       = [publish, withdraw, hide, crop_image]

admin.site.register(Event, EventAdmin)


class LogAdmin(admin.ModelAdmin):
    ordering      = ('-timestamp',)
    list_display  = ('timestamp', 'level', 'message')
    list_filter   = ('level',)
    search_fields = ('level','message')

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('level', 'message', 'timestamp')

admin.site.register(Log, LogAdmin)


class SponsorAdmin(admin.ModelAdmin):
    list_filter   = ('published',)
    list_display  = ('title', 'start', 'end', 'published',)
    search_fields = ('title',)
    actions       = [publish, withdraw]

admin.site.register(Sponsor, SponsorAdmin)
