from django.contrib import admin

from apps.experiences.models import Experience


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["user_id", "job_title", "company_name", "start_date", "end_date"]
    search_fields = ["job_title", "company_name", "user__email"]
    list_filter = ["start_date", "end_date", "company_name"]
