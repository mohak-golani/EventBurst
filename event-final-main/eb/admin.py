from django.contrib import admin
from .models import Event, Profile, EventRegistration, OrganizerProfile

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)

admin.site.register(Event, EventAdmin)
admin.site.register(Profile)
admin.site.register(EventRegistration)
admin.site.register(OrganizerProfile)