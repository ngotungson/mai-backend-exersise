from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import School, Course, Student


class TransferViewsTestCase(APITestCase):
    def setUp(self) -> None:
        self.school_test = School.objects.create(name="VietNam National University")
        self.student = Student.objects.create(name="Luong", school=self.school_test)
        self.course1 = Course.objects.create(
            name="English",
            location="VietNam",
            school=self.school_test,
        )
        self.course2 = Course.objects.create(
            name="Math",
            location="VietNam",
            school=self.school_test,
        )
        self.course1.students.add(self.student)

    def test_transfer_success(self):

        url = "/api/transfer"
        data = {
            "studentId": self.student.pk,
            "fromCourseId": self.course1.pk,
            "toCourseId": self.course2.pk,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        student_removed = (
            True if self.student not in self.course1.students.all() else False
        )
        student_added = True if self.student in self.course2.students.all() else False
        self.assertTrue(student_removed)
        self.assertTrue(student_added)

    def test_not_found_student(self):

        url = "/api/transfer"
        data = {
            "studentId": 123456789,
            "fromCourseId": self.course1.pk,
            "toCourseId": self.course2.pk,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_found_fromCourse(self):

        url = "/api/transfer"
        data = {
            "studentId": self.student.pk,
            "fromCourseId": 123456789,
            "toCourseId": self.course2.pk,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_found_toCourse(self):

        url = "/api/transfer"
        data = {
            "studentId": self.student.pk,
            "fromCourseId": self.course1.pk,
            "toCourseId": 123456789,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_found_student_in_course(self):

        url = "/api/transfer"
        data = {
            "studentId": self.student.pk,
            "fromCourseId": self.course2.pk,
            "toCourseId": self.course1.pk,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
