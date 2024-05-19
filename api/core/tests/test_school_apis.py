import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Course, School, Teacher, Student, SchoolAdministrator


class SchoolViewsTestCase(APITestCase):
    def setUp(self) -> None:
        self.school_test = School.objects.create(name="VietNam National University")
        self.teacher = Teacher.objects.create(name="Son", school=self.school_test)
        self.student = Student.objects.create(name="Luong", school=self.school_test)
        self.course = Course.objects.create(
            name="English",
            location="VietNam",
            school=self.school_test,
        )
        self.school_administrator = SchoolAdministrator.objects.create(
            name="Hung", school=self.school_test
        )

    def test_get_stats(self):
        url = f"/api/schools/{self.school_test.pk}/stats"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        teachers = data.get("teachers")
        students = data.get("students")
        courses = data.get("courses")
        school_administrator = data.get("admins")

        self.assertEqual(len(students), 1)
        self.assertEqual(len(teachers), 1)
        self.assertEqual(len(courses), 1)
        self.assertEqual(len(school_administrator), 1)
