from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Student, School


class StudentViewsTestCase(APITestCase):
    def setUp(self) -> None:
        self.base_url = "/api/students"
        self.school_test = School.objects.create(name="VietNam National University")
        self.student1 = Student.objects.create(name="Son", school=self.school_test)
        self.student2 = Student.objects.create(name="Luong", school=self.school_test)
        self.student3 = Student.objects.create(name="Hung", school=self.school_test)

    def test_get_all(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), Student.objects.count())

    def test_create(self):
        data = {
            "name": "Son",
            "school": self.school_test.pk,
        }
        response = self.client.post(self.base_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.last().name, "Son")

    def test_get_detail(self):
        url = f"{self.base_url}/{self.student1.pk}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": self.student1.pk,
                "name": self.student1.name,
                "school": self.school_test.pk,
            },
        )

    def test_update(self):
        url = f"{self.base_url}/{self.student1.pk}"
        data = {
            "name": "New student",
            "school": self.school_test.pk,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": self.student1.pk,
                "name": "New student",
                "school": self.school_test.pk,
            },
        )

    def test_delete(self):
        current_count = Student.objects.count()

        url = f"{self.base_url}/{self.student1.pk}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), current_count - 1)
