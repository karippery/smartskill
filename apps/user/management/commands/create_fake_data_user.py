from django.core.management.base import BaseCommand
from faker import Faker

from apps.user.models import User


class Command(BaseCommand):
    help = "Generates fake data for User model"

    def handle(self, *args, **kwargs):
        fake = Faker()
        num_users = 10  # Number of users you want to create
        users = []
        for _ in range(num_users):
            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            sex = fake.random_element(elements=("Male", "Female", "Non-binary"))
            title = fake.prefix()
            location = fake.city()

            # Ensure unique email addresses
            while User.objects.filter(email=email).exists():
                email = fake.email()

            users.append(
                User(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    sex=sex,
                    title=title,
                    location=location,
                )
            )

        # Bulk create users
        User.objects.bulk_create(users)

        # Set a default password for all created users
        for user in User.objects.filter(email__in=[u.email for u in users]):
            user.set_password("password123")  # Set a default password
            user.save()

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {num_users} fake users.")
        )
