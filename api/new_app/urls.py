from django.contrib import admin
from django.urls import include, path


from rest_framework import routers


from core.views.school import SchoolViewSet, transfer
from core.views.course import CourseViewSet
from core.views.teacher import TeacherViewSet
from core.views.student import StudentViewSet
from core.views.school_administrator import SchoolAdministratorViewSet


api_router = routers.DefaultRouter(trailing_slash=False)
api_router.register(r"schools", SchoolViewSet)
api_router.register(r"courses", CourseViewSet, basename="course")
api_router.register(
    r"school_administrators",
    SchoolAdministratorViewSet,
    basename="school_administrator",
)
api_router.register(r"teachers", TeacherViewSet, basename="teacher")
api_router.register(r"students", StudentViewSet, basename="student")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_router.urls)),
    path("api/transfer", transfer, name="student-transfer"),
]
