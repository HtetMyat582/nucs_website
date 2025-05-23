from django.shortcuts import render
from portal.models import News, Event
from academics.models import Course
from users.models import Faculty
from django.db.models import Q

def home(request):
    news = News.objects.all().order_by('-published_date')[:4]
    events = Event.objects.all().order_by('-date')[:4]
    return render(request, 'home.html', {'news': news, 'events': events})



def search(request):
    query = request.GET.get('q', '')
    news_results = News.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    ) if query else News.objects.none()
    event_results = Event.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ) if query else Event.objects.none()
    course_results = Course.objects.filter(
        Q(course_code__icontains=query) | Q(description__icontains=query)
    ) if query else Course.objects.none()
    faculty_results = Faculty.objects.filter(
        Q(user__username__icontains=query) | Q(department__icontains=query)
    ) if query else Faculty.objects.none()

    context = {
        'query': query,
        'news_results': news_results,
        'event_results': event_results,
        'course_results': course_results,
        'faculty_results': faculty_results,
    }
    return render(request, 'search_results.html', context)