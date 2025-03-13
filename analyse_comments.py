# Pour un lancement manuel
"""
import os
import django

# 🔹 Définir le module de configuration Django (modifie selon ton projet)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Ecopétition.settings")  # Remplace "myproject" par ton projet réel

# 🔹 Initialiser Django
django.setup()

import os
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from datetime import datetime, timedelta
from app.models import Messagerie

# Charger Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")  # Modifie selon ton projet
django.setup()
"""

import os
import django

# 🔹 Définir le module de configuration Django (modifie selon ton projet)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Ecopétition.settings")  # Remplace avec le bon nom

# 🔹 Initialiser Django
django.setup()

from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from datetime import datetime, timedelta
from app.models import Messagerie

# Charger le modèle une seule fois
model_name = "unitary/toxic-bert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)


def classify_message(text):
    """ Analyse la toxicité d'un message """
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    scores = torch.sigmoid(logits).tolist()[0]
    return {
        "toxicite": scores[0],
        "insulte": scores[2],
        "haine": scores[3],
        "menace": scores[4],
    }


def analyze_new_messages():
    """ Analyse les nouveaux messages toutes les heures """
    yadeuxheuresmdr = datetime.now() - timedelta(hours=2)

    messages = Messagerie.objects.filter(
        toxicite=0.0, insulte=0.0, haine=0.0, menace=0.0,
        date_heure__gte=yadeuxheuresmdr
    )

    count = 0
    for messagerie in messages:
        scores = classify_message(messagerie.message)
        messagerie.toxicite = scores["toxicite"]
        messagerie.insulte = scores["insulte"]
        messagerie.haine = scores["haine"]
        messagerie.menace = scores["menace"]
        messagerie.save()
        count += 1

    print(f"{count} messages analysés et mis à jour.")


if __name__ == "__main__":
    analyze_new_messages()
