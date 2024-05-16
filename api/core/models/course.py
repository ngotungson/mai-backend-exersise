from django.db import models
from .student import Student
from .teacher import Teacher
from .school import School


class Course(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    students = models.ManyToManyField(Student)
    school = models.OneToOneField(School, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
