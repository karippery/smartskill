from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from apps.projects.serializers import (
    LanguageSerializer,
    ProjectLanguageSerializer,
    ProjectRecommendSerializer,
    ProjectRoleSerializer,
    ProjectSerializer,
    ProjectSkillSerializer,
)
from apps.skills.models import UserSkill
from apps.user.models import User
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


class RecommendProjectsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectRecommendSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user_skills = self.get_user_skills(user_id)
        matching_projects = Project.objects.all()

        high_priority_users = self.get_high_priority_users(
            user_id, matching_projects, user_skills
        )
        lesser_priority_users = self.get_lesser_priority_users(
            user_id, matching_projects, user_skills
        )

        # Attach high and lesser priority users to context for serializer
        self.serializer_context = {
            "high_priority_users": high_priority_users,
            "lesser_priority_users": lesser_priority_users,
        }

        return matching_projects.distinct()

    def get_user_skills(self, user_id):
        return UserSkill.objects.filter(user_id=user_id)

    def filter_by_skills(self, queryset, user_skills):
        user_skill_ids = [user_skill.skill.id for user_skill in user_skills]
        return queryset.filter(roles__required_skills__in=user_skill_ids)

    def filter_by_skill_levels(self, queryset, user_skills):
        filters = Q()
        for user_skill in user_skills:
            filters |= Q(
                roles__projectskill__skill=user_skill.skill,
                roles__projectskill__skill_level__lte=user_skill.level,
            )
        return queryset.filter(filters)

    def filter_by_experience(self, queryset, user_id):
        user_experience_years = User.objects.get(
            id=user_id
        ).experience_years  # Assuming experience is stored in User model
        return queryset.filter(roles__experience_range__lte=user_experience_years)

    def get_high_priority_users(self, user_id, projects, user_skills):
        high_priority_users = []
        users = User.objects.all()  # Fetch all users for filtering

        for user in users:
            matched_projects = self.filter_by_skills(projects, user_skills)
            matched_projects = self.filter_by_skill_levels(
                matched_projects, user_skills
            )
            matched_projects = self.filter_by_experience(matched_projects, user.id)

            if matched_projects.exists():
                high_priority_users.append(user)

        return high_priority_users

    def get_lesser_priority_users(self, user_id, projects, user_skills):
        lesser_priority_users = []
        users = User.objects.all()  # Fetch all users for filtering

        for user in users:
            if (
                self.filter_by_skills(projects, user_skills).exists()
                or self.filter_by_skill_levels(projects, user_skills).exists()
                or self.filter_by_experience(projects, user.id).exists()
            ):
                lesser_priority_users.append(user)

        return lesser_priority_users
