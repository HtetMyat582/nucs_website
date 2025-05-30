from django.test import TestCase, Client
from django.urls import reverse
from portal.models import News, Event
from academics.models import Program, Course
from users.models import Faculty
from django.contrib.auth import get_user_model

class PortalViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.news = News.objects.create(title='Test News', content='Some content')
        self.event = Event.objects.create(title='Test Event', description='Event Desc', date='2025-06-01', time='10:00', location='Room 1')
        self.program = Program.objects.create(name='CS', degree_type='Bachelors', description='CS Program', duration_years=4)
        user = get_user_model().objects.create_user(username='faculty', password='pass', role='Faculty', first_name='Test')
        self.faculty = Faculty.objects.get(user=user)
        self.course = Course.objects.create(
            program=self.program,
            course_code='CS101',
            course_name='Test Intro CS',
            description='Basics',
            credits=3,
            faculty=self.faculty
        )

    def test_home_view(self):
        url = reverse('home')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.news.title, resp.content.decode())
        self.assertIn(self.event.title, resp.content.decode())

    def test_about_view(self):
        url = reverse('about')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_contact_view(self):
        url = reverse('contact')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_privacy_view(self):
        url = reverse('privacy')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_search_view(self):
        url = reverse('search')
        resp = self.client.get(url, {'q': 'Test'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.news.title, resp.content.decode())
        self.assertIn(self.event.title, resp.content.decode())
        self.assertIn(self.program.name, resp.content.decode())
        self.assertIn(self.course.course_name, resp.content.decode())
        self.assertIn(self.faculty.user.first_name, resp.content.decode())