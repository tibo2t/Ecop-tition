from django.db import migrations

import json
from datetime import datetime

with open(r'app\migrations\all_petitions.json', encoding='utf-8') as f:
    DATA = json.load(f)

def add_petitions_json(apps, schema_editor):

    Petition = apps.get_model('app', 'Petition')
    Theme = apps.get_model('app', 'Theme')
    User = apps.get_model('app', 'User')
    Role = apps.get_model('app', 'Role')

    # Créer ou récupérer un rôle
    role, _ = Role.objects.get_or_create(
        nom_role='User'
    )

    # Créer ou récupérer un utilisateur avec le bon `role_id`
    user, _ = User.objects.get_or_create(
        pseudo='testuser',
        defaults={'mail': 'test9@test.fr', 'password': 'hashed_password', 'role_id': role.id} 
    )

    # Récupérer un thème (ou en créer un s'il n'existe pas)
    theme, _ = Theme.objects.get_or_create(
        titre='Environnement'
    )

    petitions_dict = {}

    for data_petition in DATA:
        titre = data_petition['titre_petition']
        
        if titre not in petitions_dict:
            petitions_dict[titre] = {
                "titre": titre,
                "description": data_petition['petite_description'],
                "image_url": data_petition['image_url'],
                "date_creation": data_petition.get('date_debut', datetime.now().date()),
                "date_cloture": data_petition.get('date_fin', None),
                "theme": theme,
                "user": user
            }

    # Création des objets Petition
    petitions_to_create = [
        Petition(**petition_data) for petition_data in petitions_dict.values()
    ]

    # Insertion en une seule requête SQL
    Petition.objects.bulk_create(petitions_to_create)

def remove_all_petitions_json(apps, schema_editor):
    Petition = apps.get_model('app', 'Petition')
    for data_petition in DATA:
        Petition.objects.filter(titre=data_petition['titre_petition']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_add_roles'),
    ]

    operations = [
        migrations.RunPython(add_petitions_json, reverse_code=remove_all_petitions_json),
    ]