import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from app.models import Role, User, Petition, Theme, Signer
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'Ecopétition.settings'
django.setup()

@pytest.mark.django_db
def test_create_petition():
    client = APIClient()

    # Créer un rôle fictif
    role = Role.objects.create(nom_role="Utilisateur")

    # Créer un utilisateur fictif pour l'API avec les champs requis
    user = User.objects.create_user(
        pseudo="Valentin",  # Champ requis pour ton modèle User
        mail="Valtnin@example.com",  # Champ requis pour ton modèle User
        password="testpassword",  # Mot de passe requis
        role=role  # Associer un rôle à l'utilisateur
    )

    # Créer une pétition ou effectuer d'autres actions selon tes besoins
    petition = Petition.objects.create(
        titre="Test Petition du futur",
        description="Description de la pétition du futur",
        date_creation="2025-03-13",
        date_cloture="2025-04-13",
        theme=Theme.objects.create(titre="Environnement"),
        user=user
    )

    signer_user = User.objects.create_user(
        pseudo="Alice",  # Champ requis pour ton modèle User
        mail="alice@example.com",  # Champ requis pour ton modèle User
        password="alicepassword",  # Mot de passe requis
        role=role  # Associer un rôle à l'utilisateur
    )

    # Vérifier si la pétition a bien été créée
    assert petition.titre == "Test Petition du futur"
    assert petition.user == user

    # Se connecter en tant que signer_user pour obtenir un token JWT
    login_url = reverse('login')  # L'URL de login de ton API
    response = client.post(login_url, {'username': signer_user.pseudo, 'password': 'alicepassword'})
    assert response.status_code == 200  # Vérifier que la connexion est réussie
    
    # Récupérer le token JWT
    token = response.data['access_token']  # Si ton API retourne un champ 'access' pour le token
    
    # Ajouter le token dans les en-têtes pour l'authentification
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    # Signer la pétition en envoyant une requête POST à l'API
    url = reverse('sign-petition', kwargs={'petition_id': petition.id})
    response = client.post(url)

    # Vérifier la réponse de la signature
    assert response.status_code == 201
    assert response.data['message'] == "Pétition signée avec succès"
    
    # Vérifier que la signature a été ajoutée dans la base de données
    assert Signer.objects.filter(petition=petition, user=signer_user).exists()

    # Vérifier que l'utilisateur a bien signé la pétition
    signature = Signer.objects.get(petition=petition, user=signer_user)
    assert signature.petition == petition
    assert signature.user == signer_user
