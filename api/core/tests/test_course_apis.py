from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Course, School


class CourseViewsTestCase(APITestCase):
    def setUp(self) -> None:
        self.school_test = School.objects.create(name="VietNam National University")
        self.course1 = Course.objects.create(
            name="Math", location="VietNam", school=self.school_test
        )
        self.course2 = Course.objects.create(
            name="History", location="VietNam", school=self.school_test
        )
        self.course3 = Course.objects.create(
            name="Computer", location="VietNam", school=self.school_test
        )

    def test_get_all(self):
        url = "/api/courses"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), Course.objects.count())

    def test_create(self):
        url = "/api/courses"
        data = {
            "name": "English",
            "location": "VietNam",
            "school": self.school_test.pk,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.last().name, "English")

    def test_get_detail(self):
        url = f"/api/courses/{self.course1.pk}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": self.course1.pk,
                "name": self.course1.name,
                "location": self.course1.location,
                "school": self.school_test.pk,
                "students": [],
            },
        )

    def test_update(self):
        url = f"/api/courses/{self.course1.pk}"
        data = {
            "name": "History",
            "location": "VietNam",
            "school": self.school_test.pk,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": self.course1.pk,
                "name": "History",
                "location": "VietNam",
                "school": self.school_test.pk,
                "students": [],
            },
        )

    def test_delete(self):
        current_count = Course.objects.count()

        url = f"/api/courses/{self.course1.pk}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), current_count - 1)
