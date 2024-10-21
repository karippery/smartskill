from rest_framework import serializers

from apps.projects.models import (
    Language,
    Project,
    ProjectLanguage,
    ProjectRole,
    ProjectSkill,
)
from apps.skills.serializers import UserSkillsSerializer
from apps.user.models import User


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


class MatchedUserSerializer(serializers.ModelSerializer):
    skills = UserSkillsSerializer(source="userskill_set", many=True)
    experience_years = serializers.IntegerField()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "experience_years", "skills"]


class ProjectRecommendSerializer(serializers.ModelSerializer):
    high_priority_users = serializers.SerializerMethodField()
    lesser_priority_users = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "project_name",
            "description",
            "high_priority_users",
            "lesser_priority_users",
        ]

    def get_high_priority_users(self, project):
        # Assuming 'high_priority_users' is passed to context in view
        return MatchedUserSerializer(
            self.context.get("high_priority_users"), many=True
        ).data

    def get_lesser_priority_users(self, project):
        # Assuming 'lesser_priority_users' is passed to context in view
        return MatchedUserSerializer(
            self.context.get("lesser_priority_users"), many=True
        ).data
