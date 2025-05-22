from django.shortcuts import render
from .models import News, Event

def home(request):
    news = News.objects.all().order_by('-published_date')[:3]
    events = Event.objects.all().order_by('date')[:3]
    return render(request, 'portal/home.html', {'news': news, 'events': events})
