from rest_framework import serializers

from apps.skills.models import Skill, SkillCategory, UserSkill


class SkillCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillCategory
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['category_id', 'name']

class UserSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = ['user_id','skill_id','level']

