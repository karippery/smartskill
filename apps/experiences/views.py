from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.experiences.models import Experience
from apps.experiences.serializers import ExperienceSerializer
from core.utils.paginations import DefaultPagination
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["experiences"])
class ExperiencesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = []
    pagination_class = DefaultPagination

    def get_queryset(self):
        # Optionally, filter the queryset to the current user's experiences
        return super().get_queryset().filter(user_id=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(serializer.data)

@extend_schema(tags=["experiences"])
class ExperiencesListCreateView(generics.ListCreateAPIView):
    queryset = Experience.objects.all().order_by('start_date')
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['job_title', 'company_name', 'location']
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = Experience.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
