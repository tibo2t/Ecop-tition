import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from app.models import Petition, User
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'Ecopétition.settings'
django.setup()

@pytest.mark.django_db
def test_create_petition():
    client = APIClient()

    # Créer un utilisateur fictif pour l'API avec les champs requis
    user = User.objects.create_user(
        pseudo="testuser",  # Champ requis pour ton modèle User
        mail="testuser@example.com",  # Champ requis pour ton modèle User
        password="testpassword",  # Mot de passe requis
    )

    # Créer une pétition ou effectuer d'autres actions selon tes besoins
    petition = Petition.objects.create(
        titre="Test Petition",
        description="Description de la pétition",
        date_creation="2025-03-13",
        date_cloture="2025-04-13",
        theme=Theme.objects.create(titre="Environnement"),
        user=user
    )

    # Vérifier si la pétition a bien été créée (par exemple)
    assert petition.titre == "Test Petition"
    assert petition.user == user
