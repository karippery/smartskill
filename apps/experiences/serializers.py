from rest_framework import serializers

from apps.experiences.models import Experience
from core.cache.caches import get_user_data


class ExperienceSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id",
            "user_id",
            "user_name",
            "job_title",
            "company_name",
            "start_date",
            "end_date",
            "is_current",
            "description",
            "location",
            "skills",
            "skills_used",
        ]
        read_only_fields = ["id", "user_name", "skills"]

    def get_user_name(self, obj) -> str:
        user_info = get_user_data(obj.user_id.id)
        if user_info:
            return f"{user_info['first_name']} {user_info['last_name']}"
        return "Unknown User"

    def validate(self, data):
        if data.get("end_date") and data["start_date"] > data["end_date"]:
            raise serializers.ValidationError("End date cannot be before start date.")
        return data

    def get_skills(self, obj) -> list:
        return [skill.name for skill in obj.skills_used.all()]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")
        if request and request.method != "POST":
            representation.pop("skills_used", None)
        return representation
