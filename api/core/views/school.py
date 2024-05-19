from rest_framework import viewsets, mixins, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from django.http import JsonResponse
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status


from core.models import School, Teacher, Course, Student, SchoolAdministrator
from core.serializers import (
    SchoolSerializer,
    TeacherSerializer,
    CourseSerializer,
    StudentSerializer,
    SchoolAdministratorSerializer,
)


class SchoolViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    @action(
        methods=["get"],
        url_path="stats",
        detail=True,
        url_name="school-stats",
    )
    def get_school_stats(self, *args, **kwargs):
        """Get school stats"""
        school_id = self.kwargs["pk"]
        courses = Course.objects.filter(school_id=int(school_id))
        admins = SchoolAdministrator.objects.filter(school_id=int(school_id))
        teachers = Teacher.objects.filter(school_id=int(school_id))
        students = Student.objects.filter(school_id=int(school_id))

        json_res = {
            "id": school_id,
            "courses": CourseSerializer(courses, many=True).data,
            "admins": SchoolAdministratorSerializer(admins, many=True).data,
            "teachers": TeacherSerializer(teachers, many=True).data,
            "students": StudentSerializer(students, many=True).data,
        }

        return JsonResponse(json_res, safe=False)


@action(
    methods=["post"],
    detail=False,
    url_name="student-transfer",
)
@csrf_exempt
def transfer(request):
    body = json.loads(request.body)

    student_id = int(body.get("studentId"))
    student = Student.objects.filter(id=student_id).first()
    if not student:
        return JsonResponse(
            {"message": f"Not found student ID: {student_id}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    from_course_id = int(body.get("fromCourseId"))
    current_course = Course.objects.filter(id=from_course_id).first()
    if not current_course:
        return JsonResponse(
            {"message": f"Not found fromCourseId: {from_course_id}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    to_course_id = int(body.get("toCourseId"))
    new_course = Course.objects.filter(id=to_course_id).first()
    if not new_course:
        return JsonResponse(
            {"message": f"Not found toCourseId: {to_course_id}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if student not in current_course.students.all():
        return JsonResponse(
            {
                "message": f"Not found student {student.name} in the course: {current_course.name}"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    current_course.students.remove(student)
    new_course.students.add(student)

    return JsonResponse(
        {
            "message": f"Transfered student [{student.name}] from course [{current_course.name}]  to course [{new_course.name}] successfully"
        }
    )
