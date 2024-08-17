from rest_framework import serializers

from apps.skills.models import Skill, SkillCategory, UserSkills


class SkillCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillCategory
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    category = SkillCategorySerializer()

    class Meta:
        model = Skill
        fields = '__all__'

class UserSkillsSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = UserSkills
        fields = '__all__'
