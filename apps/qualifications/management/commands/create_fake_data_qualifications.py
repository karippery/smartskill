from django.core.management.base import BaseCommand
from faker import Faker

from apps.qualifications.models import Degree, FieldOfStudy, Qualification
from apps.user.models import User


class Command(BaseCommand):
    help = "Generates fake data for Degree and FieldOfStudy models"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create fake Degrees
        num_degrees = 10  # Number of Degree entries you want to create
        degrees = [Degree(name=fake.job()) for _ in range(num_degrees)]
        Degree.objects.bulk_create(degrees)

        # Create fake Fields of Study
        num_fields = 10  # Number of FieldOfStudy entries you want to create
        fields_of_study = [FieldOfStudy(name=fake.bs()) for _ in range(num_fields)]
        FieldOfStudy.objects.bulk_create(fields_of_study)

        users = User.objects.all()
        if not users.exists() or len(degrees) == 0 or len(fields_of_study) == 0:
            self.stdout.write(
                self.style.ERROR(
                    "Please ensure there are Users, Degrees, and Fields of Study in the database."
                )
            )
            return

        num_qualifications = 10  # Number of qualifications you want to create

        qualifications = []
        for _ in range(num_qualifications):
            qualifications.append(
                Qualification(
                    user_id=fake.random_element(users),
                    degree=fake.random_element(degrees),
                    institution=fake.company(),
                    field_of_study=fake.random_element(fields_of_study),
                    start_date=fake.date_between(start_date="-10y", end_date="-5y"),
                    end_date=fake.date_between(start_date="-4y", end_date="today"),
                    grade=fake.word(),
                    description=fake.text(),
                )
            )
        Qualification.objects.bulk_create(qualifications)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {num_degrees} fake Degrees and {num_fields} fake Fields of Study."
            )
        )
