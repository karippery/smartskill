from django.db import models
from django.forms import ValidationError

from apps.user.models import User


class SkillCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category_id = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (Category ID: {self.category_id_id})"

class UserSkill(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.SmallIntegerField()
    class Meta:
        unique_together = ('user_id', 'skill_id')

    def __str__(self):
        return f"{self.user_id.first_name} - Skill ID: {self.skill_id_id}, Level: {self.level}"

