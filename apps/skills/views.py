from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from apps.skills.models import Skill, SkillCategory, UserSkill
from apps.skills.serializers import (
    SkillCategorySerializer,
    SkillSerializer,
    UserSkillsSerializer,
)
from core.utils.paginations import DefaultPagination


@extend_schema(tags=["skill-category"])
class SkillCategoryListCreateView(generics.ListCreateAPIView):
    queryset = SkillCategory.objects.all().order_by("name")
    serializer_class = SkillCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    pagination_class = DefaultPagination


@extend_schema(tags=["skill-category"])
class SkillCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SkillCategory.objects.all().order_by("name")
    serializer_class = SkillCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    pagination_class = DefaultPagination


@extend_schema(tags=["skill"])
class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all().order_by("name")
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    pagination_class = DefaultPagination


@extend_schema(tags=["skill"])
class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all().order_by("name")
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    pagination_class = DefaultPagination


@extend_schema(tags=["user-skills"])
class UserSkillsListCreateView(generics.ListCreateAPIView):
    queryset = UserSkill.objects.all().order_by("user_id", "skill_id")
    serializer_class = UserSkillsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = []
    pagination_class = DefaultPagination


@extend_schema(tags=["user-skills"])
class UserSkillsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserSkill.objects.all().order_by("user_id", "skill_id")
    serializer_class = UserSkillsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = []
    pagination_class = DefaultPagination

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return UserSkill.objects.filter(user_id=user_id).select_related(
            "skill_id__category_id"
        )
