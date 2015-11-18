from django.contrib import admin
from .models        import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'venue', 'start', 'end', 'created')
    search_fields = ('title', 'venue')

admin.site.register(Event, EventAdmin)
