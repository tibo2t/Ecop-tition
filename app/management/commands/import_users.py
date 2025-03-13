import json
from django.core.management.base import BaseCommand
from app.models import User, Role

role_default = Role.objects.get(id=2)
class Command(BaseCommand):
    help = "Importe des utilisateurs depuis un fichier JSON"

    def handle(self, *args, **kwargs):
        file_path = '/Users/clementgueganviault/PycharmProjects/Csv/Sup de vinci/BDD_user.json'

        with open(file_path, "r", encoding="utf-8") as file:
            users = json.load(file)

        count = 0
        for user_data in users:
            if not User.objects.filter(pseudo=user_data["pseudo"]).exists():
                User.objects.create_user(
                    pseudo=user_data["pseudo"],
                    mail=user_data["email"],
                    password=user_data["password"],
                    is_active=user_data.get("is_active", True),
                    is_staff=user_data.get("is_staff", False),
                    role=role_default,
                    is_superuser=user_data.get("is_superuser", False),
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} utilisateurs importés avec succès !"))
