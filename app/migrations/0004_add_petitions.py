from django.db import migrations
from datetime import datetime, timedelta

def add_petitions(apps, schema_editor):
    Petition = apps.get_model('app', 'Petition')
    Theme = apps.get_model('app', 'Theme')
    User = apps.get_model('app', 'User')
    Role = apps.get_model('app', 'Role')  # ✅ Correction de la typo

    # Créer ou récupérer un rôle
    role, _ = Role.objects.get_or_create(
        nom_role='User'
    )

    # Créer ou récupérer un utilisateur avec le bon `role_id`
    user, _ = User.objects.get_or_create(
        pseudo='test',
        defaults={'mail': 'test3@test.fr', 'password': 'hashed_password', 'role_id': role.id}  # ✅ Utilisation de `role.id`
    )

    # Récupérer un thème (ou en créer un s'il n'existe pas)
    theme = Theme.objects.filter(titre='Environnement').first()
    if theme is None:
        theme = Theme.objects.create(titre='Environnement')

    # Ajouter une pétition dans la base de données
    Petition.objects.create(
        titre='Tous pour les cailloux',
        description='Les pauvres, on leur marche dessus !',
        date_creation=datetime.now().date(),  # ✅ Utilisation de `.date()` si `DateField`
        date_cloture=(datetime.now() + timedelta(days=15)).date(),  # ✅ Correction ici aussi
        theme=theme,
        user=user
    )

def remove_petitions(apps, schema_editor):
    Petition = apps.get_model('app', 'Petition')
    Petition.objects.filter(titre='Tous pour les cailloux').delete()  # ✅ Suppression propre

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_add_themes'),
    ]

    operations = [
        migrations.RunPython(add_petitions, reverse_code=remove_petitions),
    ]
