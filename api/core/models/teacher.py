from django.db import models
from .school import School


class Teacher(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(
        School, on_delete=models.PROTECT, blank=False, null=False
    )

    def __str__(self):
        return self.name
