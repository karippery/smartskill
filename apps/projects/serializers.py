from rest_framework import serializers

from apps.projects.models import (
    Language,
    Project,
    ProjectLanguage,
    ProjectRole,
    ProjectSkill,
)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "project_name", "description", "start_date", "end_date"]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "name"]


class ProjectRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRole
        fields = [
            "id",
            "project",
            "role_name",
            "description",
            "experience_range",
            "required_skills",
        ]


class ProjectSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSkill
        fields = ["id", "project_role", "skill", "skill_level"]


class ProjectLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLanguage
        fields = ["id", "project", "language", "skill_level"]
