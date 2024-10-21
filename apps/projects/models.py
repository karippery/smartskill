from django.db import models

from apps.skills.models import Skill
from core.common.choices import LanguageProficiencyLevel, SkillLevel


class Project(models.Model):
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    required_languages = models.ManyToManyField(
        "Language", through="ProjectLanguage", related_name="projects"
    )

    def __str__(self):
        return self.project_name

    class Meta:
        indexes = [
            models.Index(
                fields=["project_name", "start_date"]
            ),  # Indexing commonly searched fields
        ]


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProjectLanguage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    skill_level = models.SmallIntegerField(choices=LanguageProficiencyLevel.choices)

    class Meta:
        unique_together = ("project", "language")
        indexes = [
            models.Index(fields=["project", "language"]),
        ]

    def __str__(self):
        return f"{self.project.project_name} - {self.language.name}"


class ProjectRole(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="roles")
    role_name = models.CharField(max_length=255)  # e.g., Salesman
    description = models.TextField(null=True, blank=True)
    experience_range = models.IntegerField()  # e.g., "5-8 years"

    required_skills = models.ManyToManyField(
        Skill, through="ProjectSkill", related_name="project_roles"
    )

    def __str__(self):
        return f"{self.role_name} - {self.project.project_name}"

    class Meta:
        indexes = [
            models.Index(fields=["role_name", "experience_range"]),
        ]


class ProjectSkill(models.Model):
    project_role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    skill_level = models.SmallIntegerField(choices=SkillLevel.choices)

    class Meta:
        unique_together = (
            "project_role",
            "skill",
        )
        indexes = [
            models.Index(fields=["project_role", "skill"]),
        ]

    def __str__(self):
        return f"{self.project_role.role_name} - {self.skill.name}"
