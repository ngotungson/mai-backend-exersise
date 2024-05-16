from rest_framework import serializers

from core.models import School, Teacher


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["name", "address"]


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["name", "school_id"]
