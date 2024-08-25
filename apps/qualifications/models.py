from django.db import models

from apps.user.models import User

class Degree(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class FieldOfStudy(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Qualification(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qualifications')
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    institution = models.CharField(max_length=255, null=True, blank=True)
    field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    grade = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-end_date']
        indexes = [
            models.Index(fields=['user_id', 'degree']),
        ]

    constraints = [
            models.UniqueConstraint(fields=['user_id', 'degree', 'field_of_study'], name='unique_degree_field_for_user')
        ]

