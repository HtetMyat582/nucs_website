from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Student

class UsersModelsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='student', password='pass', role='Student'
        )
        self.student = Student.objects.get(user=self.user)

    def test_user_str(self):
        self.assertEqual(str(self.user), 'student')

    def test_student_str(self):
        self.assertEqual(str(self.student), 'student')
        self.assertEqual(self.student.user, self.user)