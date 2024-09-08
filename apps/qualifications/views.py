from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.qualifications.models import Degree, FieldOfStudy, Qualification
from apps.qualifications.serializers import DegreeSerializer, FieldOfStudySerializer, QualificationSerializer
from core.utils.paginations import DefaultPagination
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["qualification"])
class QualificationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['degree__name', 'institution', 'field_of_study__name']
    ordering_fields = ['start_date', 'end_date', 'institution']
    pagination_class = DefaultPagination

@extend_schema(tags=["qualification"])
class QualificationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination


@extend_schema(tags=["degree"])
class DegreeViewSet(viewsets.ModelViewSet):
    queryset = Degree.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    pagination_class = DefaultPagination
    serializer_class = DegreeSerializer

@extend_schema(tags=["field-of-study"])
class FieldOfStudyViewSet(viewsets.ModelViewSet):
    queryset = FieldOfStudy.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    pagination_class = DefaultPagination
    serializer_class = FieldOfStudySerializer