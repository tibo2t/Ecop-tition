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

    for data_petition in DATA:
        Petition.objects.create(
            titre=data_petition['titre_petition'],
            description=data_petition['petite_description'],
            image_url=data_petition['image_url'],
            date_creation=data_petition['date_debut'],
            date_cloture=data_petition['date_fin'],
            theme=theme,
            user=user
        )

def remove_all_petitions_json(apps, schema_editor):
    Petition = apps.get_model('app', 'Petition')
    for data_petition in DATA:
        Petition.objects.filter(titre=data_petition['titre_petition']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_petition_image_url'),
    ]

    operations = [
        migrations.RunPython(add_petitions_json, reverse_code=remove_all_petitions_json),
    ]