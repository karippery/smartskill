from django.core.management.base import BaseCommand
from faker import Faker

from apps.experiences.models import Experience
from apps.skills.models import Skill
from apps.user.models import User


class Command(BaseCommand):
    help = "Generates fake data for Degree and FieldOfStudy models"

    def handle(self, *args, **kwargs):
        fake = Faker()

        users = User.objects.all()
        skills = Skill.objects.all()

        num_experiences = 10  # Number of Experience entries you want to create

        for _ in range(num_experiences):
            experience = Experience(
                user_id=fake.random_element(users),
                job_title=fake.job(),
                company_name=fake.company(),
                start_date=fake.date_between(start_date="-10y", end_date="-5y"),
                end_date=fake.date_between(start_date="-4y", end_date="today"),
                is_current=fake.boolean(),
                description=fake.text(),
                location=fake.city(),
            )
            experience.save()  # Save the experience before adding many-to-many relationships
            experience.skills_used.set(
                fake.random_elements(elements=skills, length=3)
            )  # Assign random skills

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {num_experiences} fake Experiences."
            )
        )
