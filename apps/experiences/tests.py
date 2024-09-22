from datetime import date

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.experiences.models import Experience
from apps.skills.models import Skill, SkillCategory
from apps.user.models import User


class ExperiencesAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user and obtain a token
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )

        # Obtain token
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"email": "testuser@example.com", "password": "testpassword"},
        )
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.skill_category = SkillCategory.objects.create(name="Programming")
        self.skill = Skill.objects.create(
            name="Python", category_id=self.skill_category
        )
        # Create an experience
        self.experience = Experience.objects.create(
            user_id=self.user,
            job_title="Software Engineer",
            company_name="Tech Company",
            start_date=date(2020, 1, 1),
            end_date=date(2021, 1, 1),
            is_current=False,
            description="Developed software solutions.",
            location="New York",
        )
        self.experience.skills_used.set([self.skill])

    def test_create_experience(self):
        url = reverse("experiences-list")
        data = {
            "user_id": self.user.id,
            "job_title": "Software Engineer",
            "company_name": "Tech Company",
            "start_date": "2020-01-01",
            "end_date": "2021-01-01",
            "is_current": False,
            "description": "Developed software solutions.",
            "location": "New York",
            "skills_used": [self.skill.id],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_experience_list(self):
        url = reverse("experiences-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_experience(self):
        url = reverse("experiences-detail", args=[self.experience.id])
        data = {
            "user_id": self.user.id,
            "job_title": "Senior Software Engineer",
            "company_name": "Tech Company",
            "start_date": "2020-01-01",
            "end_date": "2021-01-01",
            "is_current": False,
            "description": "Developed and led software solutions.",
            "location": "New York",
            "skills_used": [self.skill.id],
        }

        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.job_title, "Senior Software Engineer")

    def test_partial_update_experience(self):
        url = reverse("experiences-detail", args=[self.experience.id])
        data = {
            "job_title": "Lead Software Engineer",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.job_title, "Lead Software Engineer")

    def test_delete_experience(self):
        url = reverse("experiences-detail", args=[self.experience.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Experience.objects.filter(id=self.experience.id).exists())
