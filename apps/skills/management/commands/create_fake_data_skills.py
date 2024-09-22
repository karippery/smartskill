from django.core.management.base import BaseCommand
from faker import Faker

from apps.skills.models import Skill, SkillCategory, UserSkill
from apps.user.models import User


class Command(BaseCommand):
    help = "Generates fake data for SkillCategory, Skill, and UserSkill models"

    def handle(self, *args, **kwargs):
        fake = Faker()
        skill_categories = [
            "Programming",
            "Design",
            "Project Management",
            "Marketing",
            "Finance",
        ]

        # Create and save SkillCategory instances
        categories = [SkillCategory(name=name) for name in skill_categories]
        SkillCategory.objects.bulk_create(categories)

        # Create Skills
        skills = []
        for category in SkillCategory.objects.all():
            for _ in range(10):
                skills.append(Skill(name=fake.word(), category_id=category))
        Skill.objects.bulk_create(skills)

        # add skill to users
        user_skills = []
        for user in User.objects.all():
            for skill in Skill.objects.all():
                user_skills.append(
                    UserSkill(
                        user_id=user,
                        skill_id=skill,
                        level=fake.random_int(min=1, max=5),
                    )
                )
        UserSkill.objects.bulk_create(user_skills)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully created fake data for SkillCategory, Skill, and UserSkill."
            )
        )
