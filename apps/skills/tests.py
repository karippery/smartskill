from django.test import TestCase
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from apps.skills.models import Skill, SkillCategory, UserSkill
from apps.user.models import User

class SkillAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user and obtain a token
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )

        # Obtain token
        response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

     # Create some initial data
        self.skill_category = SkillCategory.objects.create(name='Programming')
        self.skill = Skill.objects.create(name='Python', category_id=self.skill_category)
        self.user_skill = UserSkill.objects.create(user_id=self.user, skill_id=self.skill, level=1)

    def test_create_skill_category(self):
        url = reverse('skill-category-list-create')
        data = {'name': 'Design'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SkillCategory.objects.count(), 2)
        self.assertEqual(SkillCategory.objects.last().name, 'Programming')

    def test_list_skill_categories(self):
        url = reverse('skill-category-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_skill_category(self):
        url = reverse('skill-category-detail', kwargs={'pk': self.skill_category.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.skill_category.name)

    def test_create_skill(self):
        url = reverse('skill-list-create')
        data = {'name': 'JavaScript', 'category_id': self.skill_category.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_skills(self):
        url = reverse('skill-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_skill(self):
        url = reverse('skill-detail', kwargs={'pk': self.skill.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_skill(self):
        url = reverse('user-skills-list-create')
        data = {
            'user_id': self.user.id,
            'skill_id': self.skill.id,
            'level': 2
        }
        UserSkill.objects.filter(user_id=self.user.id, skill_id=self.skill.id).delete()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserSkill.objects.count(), 1)
        self.assertEqual(UserSkill.objects.last().level, 2)

    def test_list_user_skills(self):
        url = reverse('user-skills-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_user_skill(self):
        url = reverse('user-skills-detail', kwargs={'pk': self.user_skill.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['skill_name'], self.user_skill.skill_id.name)

    def test_user_skills_details(self):
        url = reverse('user-skills', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


