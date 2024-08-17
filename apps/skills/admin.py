from django.contrib import admin

from apps.skills.models import Skill, SkillCategory, UserSkills


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(UserSkills)
class UserSkillsAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_skills', 'level')
    search_fields = ('user__email', 'skills__name')
    filter_horizontal = ('skills',)

    def get_skills(self, obj):
        return ", ".join([skill.name for skill in obj.skills.all()])
    get_skills.short_description = 'Skills'

