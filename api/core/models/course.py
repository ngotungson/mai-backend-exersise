from django.db import models
from .student import Student
from .teacher import Teacher
from .school import School


class Course(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    students = models.ManyToManyField(Student, null=True)
    school = models.ForeignKey(
        School, on_delete=models.PROTECT, blank=False, null=False
    )

    def __str__(self):
        return self.name
