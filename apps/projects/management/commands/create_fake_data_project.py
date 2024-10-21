import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from faker import Faker

from apps.projects.models import (
    Language,
    Project,
    ProjectLanguage,
    ProjectRole,
    ProjectSkill,
)
from apps.skills.models import Skill
from core.common.choices import LanguageProficiencyLevel, SkillLevel


class Command(BaseCommand):
    help = "Generates fake data for Project-related models"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create some languages if they don't already exist
        num_languages = 5
        languages = []
        for _ in range(num_languages):
            language_name = fake.language_name()
            # Check if language already exists
            language, created = Language.objects.get_or_create(name=language_name)
            languages.append(language)

        # Get existing skills from the database
        skills = Skill.objects.all()
        if not skills:
            self.stdout.write(self.style.WARNING("No skills found in the database."))
            return  # Exit if there are no skills

        # Create projects
        num_projects = 10
        projects = []
        for _ in range(num_projects):
            project_name = fake.company()
            description = fake.text()
            start_date = fake.date_this_decade()
            end_date = start_date + timedelta(days=random.randint(30, 365))
            project = Project.objects.create(
                project_name=project_name,
                description=description,
                start_date=start_date,
                end_date=end_date,
            )
            projects.append(project)

            # Assign random languages to the project
            for lang in random.sample(languages, random.randint(1, num_languages)):
                ProjectLanguage.objects.get_or_create(
                    project=project,
                    language=lang,
                    skill_level=random.choice(LanguageProficiencyLevel.values),
                )

        # Create roles for each project
        for project in projects:
            num_roles = random.randint(1, 3)
            for _ in range(num_roles):
                role_name = fake.job()
                description = fake.text()
                experience_range = random.randint(1, 10)
                project_role = ProjectRole.objects.create(
                    project=project,
                    role_name=role_name,
                    description=description,
                    experience_range=experience_range,
                )

                # Assign random skills to the role
                for skill in random.sample(
                    list(skills), random.randint(1, len(skills))
                ):
                    ProjectSkill.objects.get_or_create(
                        project_role=project_role,
                        skill=skill,
                        skill_level=random.choice(SkillLevel.values),
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {num_projects} fake projects with roles and skills."
            )
        )
