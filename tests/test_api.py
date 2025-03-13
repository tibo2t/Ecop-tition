import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from app.models import Petition, User

@pytest.mark.django_db
def test_create_petition():
    client = APIClient()

    # Créer un utilisateur fictif pour l'API
    user = User.objects.create_user(username="testuser", password="testpass")

    # Données à envoyer
    data = {
        "titre": "Protégeons la nature",
        "description": "Une pétition pour sauver la forêt",
        "date_creation": "2025-03-11",
        "date_cloture": "2025-03-26",
        "user": user.id,  # Associe la pétition à l'utilisateur
    }

    # Envoie une requête POST à l'endpoint
    url = reverse("petition-list")  # Assure-toi que l'URL correspond à ton projet
    response = client.post(url, data, format="json")

    # Vérifications
    assert response.status_code == 201  # Vérifie si la requête a réussi
    assert response.data["titre"] == data["titre"]
