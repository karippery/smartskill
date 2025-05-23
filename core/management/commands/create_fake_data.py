from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create fake data for all apps"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating fake data for users...")
        call_command("create_fake_data_user")

        self.stdout.write("Creating fake data for skills...")
        call_command("create_fake_data_skills")

        self.stdout.write("Creating fake data for qualifications...")
        call_command("create_fake_data_qualifications")

        self.stdout.write("Creating fake data for experiences...")
        call_command("create_fake_data_experiences")

        self.stdout.write("Creating fake data for projects...")
        call_command("create_fake_data_projects")

        self.stdout.write(
            self.style.SUCCESS("Successfully created fake data for all apps")
        )
