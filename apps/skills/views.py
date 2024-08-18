from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.skills.models import Skill, SkillCategory, UserSkill
from apps.skills.serializers import SkillCategorySerializer, SkillSerializer, UserSkillsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.utils.paginations import DefaultPagination

class SkillCategoryListCreateView(generics.ListCreateAPIView):
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    pagination_class = DefaultPagination

class SkillCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    pagination_class = DefaultPagination

class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    pagination_class = DefaultPagination

class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    pagination_class = DefaultPagination

class UserSkillsListCreateView(generics.ListCreateAPIView):
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = []
    pagination_class = DefaultPagination

class UserSkillsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = []
    pagination_class = DefaultPagination
