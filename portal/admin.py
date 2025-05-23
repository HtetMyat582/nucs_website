from django.contrib import admin
from .models import News, Event

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'published_date')
    list_filter = ('title', 'content', 'published_date')
    search_fields = ('title', 'content', 'published_date')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    list_filter = ('title', 'date', 'location')
    search_fields = ('title', 'date', 'location')