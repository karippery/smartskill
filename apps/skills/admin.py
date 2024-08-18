from django.contrib import admin
from apps.skills.models import Skill, SkillCategory, UserSkill

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(UserSkill)
class UserSkillsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'get_skills', 'level')
    search_fields = ('user_id__email', 'skill_id__name')

    def get_skills(self, obj):
        return obj.skill_id.name
    get_skills.short_description = 'Skills'

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_category')
    search_fields = ('name', 'category_id__name')
    list_filter = ('category_id',)

    def get_category(self, obj):
        return obj.category_id.name
    get_category.short_description = 'Category'
