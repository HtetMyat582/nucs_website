from django.shortcuts import render
from portal.models import News, Event
from academics.models import Course, Program
from users.models import Faculty
from django.db.models import Q
from datetime import datetime

def home(request):
    news = News.objects.all().order_by('-published_date')[:4]
    events = Event.objects.all().order_by('-date')[:4]
    now = datetime.now().year
    return render(request, 'home.html', {'news': news, 'events': events, 'now': now})

def about(request):
    now = datetime.now().year
    return render(request, 'about.html', {'now': now})

def contact(request):
    now = datetime.now().year
    return render(request, 'contact.html', {'now': now})

def privacy(request):
    now = datetime.now().year
    return render(request, 'privacy.html', {'now': now})

def search(request):
    query = request.GET.get('q', '')
    news_results = News.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    ) if query else News.objects.none()
    event_results = Event.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ) if query else Event.objects.none()
    program_results = Program.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query) | Q(degree_type__icontains=query)
    ) if query else Program.objects.none()
    course_results = Course.objects.filter(
        Q(course_code__icontains=query) | Q(description__icontains=query) | Q(course_name__icontains=query)
    ) if query else Course.objects.none()
    faculty_results = Faculty.objects.filter(
        Q(user__username__icontains=query) | Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) | Q(department__icontains=query)
    ) if query else Faculty.objects.none()

    context = {
        'query': query,
        'news_results': news_results,
        'event_results': event_results,
        'program_results': program_results,
        'course_results': course_results,
        'faculty_results': faculty_results,
    }
    return render(request, 'search_results.html', context)