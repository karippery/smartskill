from django.db import models

from apps.user.models import User


class Experience(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="experiences"
    )
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    skills_used = models.ManyToManyField("skills.Skill", blank=True)

    class Meta:
        ordering = ["-start_date"]
