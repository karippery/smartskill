from apps.experiences.models import Experience
from rest_framework import serializers
from apps.skills.serializers import SkillSerializer


class ExperienceSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = ['id', 'user_id', 'user_name', 'job_title', 'company_name', 'start_date', 'end_date', 'is_current', 'description', 'location', 'skills', 'skills_used']
        read_only_fields = ['id', 'user_name', 'skills']

    def get_user_name(self, obj):
        return obj.user_id.first_name

    def get_skills(self, obj):
        return SkillSerializer(obj.skills_used, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.method != 'POST':
            representation.pop('skills_used', None)
        return representation
