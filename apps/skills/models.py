from django.db import models

from apps.user.models import User
from core.common.choices import SkillLevel


class SkillCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category_id = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (Category ID: {self.category_id_id})"


class UserSkill(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.SmallIntegerField(choices=SkillLevel.choices)

    class Meta:
        unique_together = ("user_id", "skill_id")
        ordering = ["user_id", "skill_id"]

    def __str__(self):
        return f"{self.user.first_name} - Skill: {self.skill.name}, Level: {self.get_level_display()}"
