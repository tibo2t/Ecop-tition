from django.db import migrations
from datetime import datetime, timedelta

def add_messagerie(apps, schema_editor):
    Petition = apps.get_model('app', 'Petition')
    User = apps.get_model('app', 'User')
    Messagerie = apps.get_model('app', 'Messagerie')
    Theme = apps.get_model('app', 'Theme')
    Role = apps.get_model('app', 'Role')

    # Créer ou récupérer un rôle
    role, _ = Role.objects.get_or_create(
        nom_role='User'
    )

    # Récupérer un thème (ou en créer un s'il n'existe pas)
    theme, _ = Theme.objects.get_or_create(
        titre='Environnement'
    )
    
    # Créer ou récupérer un utilisateur avec le bon `role_id`
    user, _ = User.objects.get_or_create(
        pseudo='test',
        defaults={'mail': 'test3@test.fr', 'password': 'hashed_password', 'role_id': role.id}  # ✅ Utilisation de `role.id`
    )

    # Créer ou récupérer une pétition
    petition, _ = Petition.objects.get_or_create(
        titre='Tous pour les cailloux',
        defaults={'description': 'Les pauvres, on leur marche dessus !', 'date_creation': '2025-03-11', 'date_cloture': '2025-03-26', 'theme_id': theme.id, 'user.id': user.id}  # ✅ Utilisation de `role.id`
    )

    # Ajouter un message dans la base de données
    Messagerie.objects.create(
        petition=petition,
        user=user,
        date_heure=datetime.now().date(),  # ✅ Utilisation de `.date()` si `DateField`
        message='Je valide fort cette pétition!'
    )

def remove_messagerie(apps, schema_editor):
    Messagerie = apps.get_model('app', 'Messagerie')
    Messagerie.objects.filter(message='Je valide fort cette pétition!').delete()  # ✅ Suppression propre

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_add_roles'),
    ]

    operations = [
        migrations.RunPython(add_messagerie, reverse_code=remove_messagerie),
    ]