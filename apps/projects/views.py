from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from apps.projects.serializers import (
    LanguageSerializer,
    ProjectLanguageSerializer,
    ProjectRoleSerializer,
    ProjectSerializer,
    ProjectSkillSerializer,
)
from core.utils.paginations import DefaultPagination

from .models import Language, Project, ProjectLanguage, ProjectRole, ProjectSkill


@extend_schema(tags=["project"])
class ProjectViewSet(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["project_name", "start_date", "required_languages"]
    pagination_class = DefaultPagination


@extend_schema(tags=["project"])
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer


@extend_schema(tags=["language"])
class LanguageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    pagination_class = DefaultPagination


@extend_schema(tags=["language"])
class LanguageRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


@extend_schema(tags=["project-role"])
class ProjectRoleListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProjectRole.objects.all()
    serializer_class = ProjectRoleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["role_name"]
    pagination_class = DefaultPagination


@extend_schema(tags=["project-role"])
class ProjectRoleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectRole.objects.all()
    serializer_class = ProjectRoleSerializer


@extend_schema(tags=["project-language"])
class ProjectLanguageListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProjectLanguage.objects.all()
    serializer_class = ProjectLanguageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["project", "language"]
    pagination_class = DefaultPagination


@extend_schema(tags=["project-language"])
class ProjectLanguageRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = ProjectLanguage.objects.all()
    serializer_class = ProjectLanguageSerializer


@extend_schema(tags=["project-skill"])
class ProjectSkillListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProjectSkill.objects.all()
    serializer_class = ProjectSkillSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["project_role", "skill"]
    pagination_class = DefaultPagination


@extend_schema(tags=["project-skill"])
class ProjectSkillRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectSkill.objects.all()
    serializer_class = ProjectSkillSerializer
