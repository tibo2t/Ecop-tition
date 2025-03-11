from django.db import migrations

def add_themes(apps, schema_editor):
    Theme = apps.get_model('app', 'Theme')
    # Ajoute des rôles dans la base de données
    Theme.objects.create(titre='Environnement')
    Theme.objects.create(titre='Santé')

def remove_themes(apps, schema_editor):
    Theme = apps.get_model('app', 'Theme')
    # Supprime les rôles ajoutés
    Theme.objects.filter(titre__in=['Environnement', 'Santé']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_add_roles'),
    ]

    operations = [
        migrations.RunPython(add_themes, reverse_code=remove_themes),
    ]
