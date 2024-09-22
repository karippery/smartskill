from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.projects.models import Language, Project, ProjectLanguage, ProjectRole
from apps.skills.models import Skill, SkillCategory
from apps.user.models import User


class TestProjectsAPI(TestCase):
    def setUp(self):
        # Setup APIClient
        self.client = APIClient()

        # Create a user and authenticate
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )

        # Obtain token for authentication
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"email": "testuser@example.com", "password": "testpassword"},
        )
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        # Create a sample project
        self.project = Project.objects.create(
            project_name="Test Project",
            description="A project for testing",
            start_date="2024-01-01",
            end_date="2024-12-31",
        )

        # Create a sample language
        self.language = Language.objects.create(name="English")

        # Create a sample skill
        self.skill_category = SkillCategory.objects.create(name="Programming")
        self.skill = Skill.objects.create(
            name="Python", category_id=self.skill_category
        )

    def test_create_language(self):
        url = reverse("language-list-create")
        data = {"name": "Spanish"}
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Spanish"

    def test_create_project_language(self):
        url = reverse("project-language-list")
        data = {
            "project": self.project.id,
            "language": self.language.id,
            "skill_level": 2,
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["project"] == self.project.id
        assert response.data["language"] == self.language.id
        assert response.data["skill_level"] == 2

    def test_create_project_role(self):
        url = reverse("project-role-list-create")
        data = {
            "project": self.project.id,
            "role_name": "Developer",
            "experience_range": 5,
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["role_name"] == "Developer"
        assert response.data["experience_range"] == 5

    def test_create_project_skill(self):
        project_role = ProjectRole.objects.create(
            project=self.project, role_name="Developer", experience_range=5
        )
        url = reverse("project-skill-list")
        data = {
            "project_role": project_role.id,
            "skill": self.skill.id,
            "skill_level": 2,
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["project_role"] == project_role.id
        assert response.data["skill"] == self.skill.id
        assert response.data["skill_level"] == 2

    def test_patch_project_role(self):
        project_role = ProjectRole.objects.create(
            project=self.project, role_name="Manager", experience_range=8
        )

        url = reverse("project-role-detail", args=[project_role.id])
        patch_data = {"role_name": "Senior Manager", "experience_range": 10}
        response = self.client.patch(url, patch_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["role_name"] == "Senior Manager"
        assert response.data["experience_range"] == 10

    def test_delete_project_language(self):
        project_language = ProjectLanguage.objects.create(
            project=self.project,
            language=self.language,
            skill_level=2,
        )

        url = reverse("project-language-detail", args=[project_language.id])
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
