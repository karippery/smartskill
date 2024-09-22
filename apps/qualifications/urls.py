from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.qualifications.views import (
    DegreeViewSet,
    FieldOfStudyViewSet,
    QualificationListCreateAPIView,
    QualificationRetrieveUpdateDestroyAPIView,
)

router = DefaultRouter()
router.register(r"degrees", DegreeViewSet, basename="degree")
router.register(r"fields-of-study", FieldOfStudyViewSet, basename="fieldofstudy")


urlpatterns = [
    path(
        "", QualificationListCreateAPIView.as_view(), name="qualification-list-create"
    ),
    path(
        "<int:pk>/",
        QualificationRetrieveUpdateDestroyAPIView.as_view(),
        name="qualification-detail",
    ),
    path("", include(router.urls)),
]
