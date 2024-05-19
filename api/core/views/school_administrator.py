from rest_framework import viewsets

from core.models import SchoolAdministrator
from core.serializers import (
    SchoolAdministratorSerializer,
)


class SchoolAdministratorViewSet(viewsets.ModelViewSet):
    queryset = SchoolAdministrator.objects.all()
    serializer_class = SchoolAdministratorSerializer
