from django.contrib import admin
from .models import Event, Category, Participant

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'category', 'image')

# Register models
admin.site.register(Event, EventAdmin)  # Use EventAdmin for Event
admin.site.register(Category)
admin.site.register(Participant)