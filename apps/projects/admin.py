from django.contrib import admin

from apps.projects.models import (
    Language,
    Project,
    ProjectLanguage,
    ProjectRole,
    ProjectSkill,
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "project_name",
        "start_date",
        "end_date",
        "created_at",
        "updated_at",
    )
    search_fields = ("project_name", "start_date")
    list_filter = ("start_date", "end_date")
    ordering = ("start_date",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ProjectRole)
class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = ("role_name", "project", "experience_range")
    search_fields = ("role_name", "project__project_name")
    list_filter = ("experience_range",)
    ordering = ("role_name",)


@admin.register(ProjectLanguage)
class ProjectLanguageAdmin(admin.ModelAdmin):
    list_display = ("project", "language", "skill_level")
    search_fields = ("project__project_name", "language__name")
    list_filter = ("skill_level",)
    ordering = ("project", "language")


@admin.register(ProjectSkill)
class ProjectSkillAdmin(admin.ModelAdmin):
    list_display = ("project_role", "skill", "skill_level")
    search_fields = ("project__project_name", "skill__name")
    list_filter = ("skill_level",)
    ordering = ("project_role", "skill")
