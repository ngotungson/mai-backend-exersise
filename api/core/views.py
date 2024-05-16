from rest_framework import viewsets, mixins

from core.models import School, Teacher
from core.serializers import SchoolSerializer, TeacherSerializer


class SchoolViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class TeacherViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
