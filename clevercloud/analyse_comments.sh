#!/bin/bash -l

# Se rendre dans le dossier de l'application
cd ${APP_HOME}

# Activer l'environnement virtuel (si utilisé)
source venv/bin/activate  # Ajuste selon ton projet

# Exécuter le script d'analyse
python analyze_comments.py
