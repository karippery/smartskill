from django.db import models

from apps.user.models import User


class SkillCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class UserSkills(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill)
    level = models.IntegerField()

    def __str__(self):
        return f"{self.user.first_name} - Level {self.level}"