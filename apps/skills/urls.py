
from apps.skills.views import SkillCategoryDetailView, SkillCategoryListCreateView, SkillDetailView, SkillListCreateView, UserSkillsDetailAPIView, UserSkillsDetailView, UserSkillsListCreateView
from django.urls import path

urlpatterns = [
    path('skills-categories/', SkillCategoryListCreateView.as_view(), name='skill-category-list-create'),
    path('skills-categories/<int:pk>/', SkillCategoryDetailView.as_view(), name='skill-category-detail'),
    path('skills/', SkillListCreateView.as_view(), name='skill-list-create'),
    path('skills/<int:pk>/', SkillDetailView.as_view(), name='skill-detail'),
    path('user-skills/', UserSkillsListCreateView.as_view(), name='user-skills-list-create'),
    path('user-skills/<int:pk>/', UserSkillsDetailView.as_view(), name='user-skills-detail'),
    path('user-skills/details/<int:user_id>/', UserSkillsDetailAPIView.as_view(), name='user-skills'),
]