import csv
from django.core.management.base import BaseCommand
from app.models import Messagerie
from datetime import datetime

class Command(BaseCommand):
    help = "Importe les commentaires depuis un fichier CSV"

    def handle(self, *args, **kwargs):
        file_path = '/Users/clementgueganviault/PycharmProjects/Csv/Sup de vinci/commentaires.csv'

        with open(file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:

                date_heure = datetime.strptime(row["date_heure"], "%Y-%m-%d %H:%M:%S")

                Messagerie.objects.create(
                    message=row["message"],
                    date_heure=date_heure,
                    petition_id=int(row["petition_id"]),
                    user_id=int(row["user_id"]),
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} commentaires importés avec succès !"))

