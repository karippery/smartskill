from django.urls import path

from .views import ExperiencesDetailView, ExperiencesListCreateView

urlpatterns = [
    path("<int:pk>/", ExperiencesDetailView.as_view(), name="experiences-detail"),
    path("", ExperiencesListCreateView.as_view(), name="experiences-list"),
]
