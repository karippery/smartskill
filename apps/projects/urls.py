from django.urls import path

from apps.projects.views import (
    LanguageListCreateAPIView,
    LanguageRetrieveUpdateDestroyAPIView,
    ProjectDetailView,
    ProjectLanguageListCreateAPIView,
    ProjectLanguageRetrieveUpdateDestroyAPIView,
    ProjectRoleListCreateAPIView,
    ProjectRoleRetrieveUpdateDestroyAPIView,
    ProjectSkillListCreateAPIView,
    ProjectSkillRetrieveUpdateDestroyAPIView,
    ProjectViewSet,
    RecommendProjectsView,
)

urlpatterns = [
    path("", ProjectViewSet.as_view(), name="project-list-create"),
    path("/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path(
        "languages/", LanguageListCreateAPIView.as_view(), name="language-list-create"
    ),
    path(
        "languages/<int:pk>/",
        LanguageRetrieveUpdateDestroyAPIView.as_view(),
        name="language-detail",
    ),
    path(
        "project-roles/",
        ProjectRoleListCreateAPIView.as_view(),
        name="project-role-list-create",
    ),
    path(
        "project-roles/<int:pk>/",
        ProjectRoleRetrieveUpdateDestroyAPIView.as_view(),
        name="project-role-detail",
    ),
    path(
        "project-languages/",
        ProjectLanguageListCreateAPIView.as_view(),
        name="project-language-list",
    ),
    path(
        "project-languages/<int:pk>/",
        ProjectLanguageRetrieveUpdateDestroyAPIView.as_view(),
        name="project-language-detail",
    ),
    path(
        "project-skills/",
        ProjectSkillListCreateAPIView.as_view(),
        name="project-skill-list",
    ),
    path(
        "project-skills/<int:pk>/",
        ProjectSkillRetrieveUpdateDestroyAPIView.as_view(),
        name="project-skill-detail",
    ),
    path(
        "project-recommended/<int:pk>/",
        RecommendProjectsView.as_view(),
        name="project-recommended",
    ),
]
