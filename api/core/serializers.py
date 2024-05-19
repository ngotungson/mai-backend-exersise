from rest_framework import serializers

from core.models import School, Teacher, Course, Student, SchoolAdministrator


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["id", "name", "address"]


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class SchoolAdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolAdministrator
        fields = "__all__"
