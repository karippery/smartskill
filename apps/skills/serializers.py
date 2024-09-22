from rest_framework import serializers

from apps.skills.models import Skill, SkillCategory, UserSkill


class SkillCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillCategory
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "category_id", "name"]


class UserSkillsSerializer(serializers.ModelSerializer):
    category_id = serializers.CharField(
        source="skill_id.category_id.id", read_only=True
    )
    category_name = serializers.CharField(
        source="skill_id.category_id.name", read_only=True
    )
    skill_name = serializers.CharField(source="skill_id.name", read_only=True)

    class Meta:
        model = UserSkill
        fields = [
            "id",
            "category_id",
            "category_name",
            "user_id",
            "skill_id",
            "skill_name",
            "level",
        ]
