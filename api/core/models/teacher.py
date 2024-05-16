from django.db import models
from .school import School


class Teacher(models.Model):
    name = models.CharField(max_length=255)
    school = models.OneToOneField(School, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name
