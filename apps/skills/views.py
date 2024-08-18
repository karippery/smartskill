
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.skills.models import Skill, SkillCategory, UserSkill
from apps.skills.serializers import SkillCategorySerializer, SkillSerializer, UserSkillsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.user.models import User
from core.utils.paginations import DefaultPagination
from rest_framework.response import Response
from rest_framework import status
class SkillCategoryListCreateView(generics.ListCreateAPIView):
    queryset = SkillCategory.objects.all().order_by('name')
    serializer_class = SkillCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    pagination_class = DefaultPagination

class SkillCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SkillCategory.objects.all().order_by('name')
    serializer_class = SkillCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    pagination_class = DefaultPagination

class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all().order_by('name')
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    pagination_class = DefaultPagination

class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all().order_by('name')
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    pagination_class = DefaultPagination

class UserSkillsListCreateView(generics.ListCreateAPIView):
    queryset = UserSkill.objects.all().order_by('user_id', 'skill_id')
    serializer_class = UserSkillsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = []
    pagination_class = DefaultPagination

class UserSkillsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserSkill.objects.all().order_by('user_id', 'skill_id')
    serializer_class = UserSkillsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = []
    pagination_class = DefaultPagination

class UserSkillsDetailAPIView(generics.ListAPIView):
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = []
    pagination_class = DefaultPagination

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return UserSkill.objects.filter(user_id=user_id).select_related('skill_id__category_id')
