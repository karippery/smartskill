from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.qualifications.models import Degree, FieldOfStudy, Qualification
from apps.user.models import User


class QualificationsAPITests(APITestCase):
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

        self.degree = Degree.objects.create(name="Bachelor of Science")
        self.field_of_study = FieldOfStudy.objects.create(name="Computer Science")

        # Create a qualification
        self.qualification = Qualification.objects.create(
            user_id=self.user,
            degree=self.degree,
            institution="Tech University",
            field_of_study=self.field_of_study,
            start_date=date(2018, 9, 1),
            end_date=date(2022, 6, 30),
            grade="A",
            description="Studied computer science.",
        )

    def test_create_qualification(self):
        url = reverse("qualification-list-create")
        data = {
            "user_id": self.user.id,
            "degree": self.degree.id,
            "institution": "Tech University",
            "field_of_study": self.field_of_study.id,
            "start_date": "2018-09-01",
            "end_date": "2022-06-30",
            "grade": "A",
            "description": "Studied computer science.",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_qualification(self):
        url = reverse("qualification-detail", args=[self.qualification.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.qualification.id)

    def test_update_qualification(self):
        url = reverse("qualification-detail", args=[self.qualification.id])
        data = {"institution": "Updated University", "grade": "A+"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.qualification.refresh_from_db()
        self.assertEqual(self.qualification.institution, "Updated University")
        self.assertEqual(self.qualification.grade, "A+")

    def test_delete_qualification(self):
        url = reverse("qualification-detail", args=[self.qualification.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Qualification.objects.filter(id=self.qualification.id).exists()
        )
