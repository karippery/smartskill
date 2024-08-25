from django.contrib import admin
from .models import Degree, FieldOfStudy, Qualification

@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(FieldOfStudy)
class FieldOfStudyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'degree', 'institution', 'field_of_study', 'start_date', 'end_date']
    search_fields = ['user_id__first_name', 'institution', 'degree__name', 'field_of_study__name']