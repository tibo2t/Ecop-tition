🍃 EcoPetition - Backend Django
============================
Description
-----------
EcoPetition est une API REST développée avec **Django** et **Django REST Framework** pour gérer un système de pétitions en ligne. Les utilisateurs peuvent créer des pétitions, y ajouter des messages et interagir avec d'autres utilisateurs.
Technologies utilisées
----------------------

-   **Python 3.11+**
-   **Django 5.1**
-   **Django REST Framework**
-   **SQLite / PostgreSQL**
-   **JWT Authentication**

⚙️ Installation & Configuration
----------------------------
### 1\. Cloner le repo
```
 git clone https://github.com/ton-repo/ecop-tition-backend.git
 cd ecop-tition-backend
```

### 2\. Installer les dépendances
```
 pip install -r requirements.txt
```
### 3\. Configurer la base de données
-   Par défaut, SQLite est utilisé.
-   Pour PostgreSQL, modifier **settings.py** avec vos accès DB.
Appliquer les migrations :
```
 python manage.py migrate
```

### 4\. Lancer le serveur
```
 python manage.py runserver
```

 Endpoints API
-------------
### ✔️ Authentification
-   `POST /api/user/register/` - Inscription
-   `POST /api/user/login/` - Connexion
-   `POST /api/user/verify/` - Vérification du token JWT

### 📚 Thèmes
-   `GET /api/themes/` - Liste des thèmes
-   `POST /api/petitions/create/` - Créer un thème
-   `DELETE /api/petitions/delete/{id}/` - Supprimer une pétition
  
### 📝 Pétitions
-   `POST /api/petitions/` - Liste des pétitions
-   `GET /api/petitions/{id}/sign_count` - Lister le nombre de signature d'une pétition
-   `GET /api/petitions/{id}/` - Détails d'une pétition
-   `DELETE /api/petitions/list/paginated/` - Lister les pétitions par lot de 12

### ✏️ Signature
-   `POST /api/petitions/{id}/sign` - Signer une pétition
-   `GET /api/petitions/{id}/sign_count` - Lister le nombre de signature d'une pétition

### 📩 Messagerie
-   `GET /api/messagerie/` - Liste des messages
-   `POST /api/messagerie/create/` - Créer une message
-   `DELETE /api/messagerie/{id}/delete/` - Supprimer un message

Contribution
------------
1.  **Fork** le projet
2.  **Crée une branche** : `git checkout -b ma-feature`
3.  **Fais tes modifs** et commit : `git commit -m "Ajout d'une feature"`
4.  **Push** : `git push origin ma-feature`
5.  **Ouvre une Pull Request** 🚀

test
Licence
-------
Ce projet est sous licence **MIT**.

