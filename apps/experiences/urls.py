from django.urls import path
from .views import ExperiencesDetailView, ExperiencesListCreateView

urlpatterns = [
    path('experiences/<int:pk>/', ExperiencesDetailView.as_view(), name='experiences-detail'),
    path('experiences/', ExperiencesListCreateView.as_view(), name='experiences-list'),
]