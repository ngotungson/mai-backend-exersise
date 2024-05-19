from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Teacher, School


class TeacherViewsTestCase(APITestCase):
    def setUp(self) -> None:
        self.school_test = School.objects.create(name="VietNam National University")
        self.teacher1 = Teacher.objects.create(name="Son", school=self.school_test)
        self.teacher2 = Teacher.objects.create(name="Luong", school=self.school_test)
        self.teacher3 = Teacher.objects.create(name="Hung", school=self.school_test)

    def test_get_all(self):
        url = "/api/teachers"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), Teacher.objects.count())

    def test_create(self):
        url = "/api/teachers"
        data = {
            "name": "Son",
            "school": self.school_test.pk,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.last().name, "Son")

    def test_get_detail(self):
        url = f"/api/teachers/{self.teacher1.pk}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": self.teacher1.pk,
                "name": self.teacher1.name,
                "school": self.school_test.pk,
            },
        )

    def test_update(self):
        url = f"/api/teachers/{self.teacher1.pk}"
        data = {
            "name": "New teacher",
            "school": self.school_test.pk,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": self.teacher1.pk,
                "name": "New teacher",
                "school": self.school_test.pk,
            },
        )

    def test_delete(self):
        current_count = Teacher.objects.count()

        url = f"/api/teachers/{self.teacher1.pk}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Teacher.objects.count(), current_count - 1)
