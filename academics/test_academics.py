from django.test import TestCase
from academics.models import Program, Course
from users.models import Faculty
from django.contrib.auth import get_user_model

class AcademicsModelsTest(TestCase):
    def setUp(self):
        self.program = Program.objects.create(
            name='CS',
            degree_type='Bachelors',
            description='CS Program',
            duration_years=4
        )
        user = get_user_model().objects.create_user(username='Faculty', password='pass', role='Faculty')
        self.faculty = Faculty.objects.get(user=user)
        self.course = Course.objects.create(
            program=self.program,
            course_code='CS101',
            course_name='Intro CS',
            description='Basics',
            credits=3,
            faculty=self.faculty
        )

    def test_program_str(self):
        self.assertEqual(str(self.program), 'CS')

    def test_course_str(self):
        self.assertEqual(str(self.course), 'Intro CS')
        self.assertEqual(self.course.program, self.program)
        self.assertEqual(self.course.faculty, self.faculty)