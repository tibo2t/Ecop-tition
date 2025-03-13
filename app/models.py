from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Modèle Role
class Role(models.Model):
    nom_role = models.CharField(max_length=50)

    def __str__(self):
        return self.nom_role

class UserManager(BaseUserManager):
    def create_user(self, pseudo, mail, password=None, **extra_fields):
        if not mail:
            raise ValueError("L'adresse email est obligatoire")
        mail = self.normalize_email(mail)
        user = self.model(pseudo=pseudo, mail=mail, **extra_fields)
        user.set_password(password)  # Hash du mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, pseudo, mail, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(pseudo, mail, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    pseudo = models.CharField(max_length=50, unique=True)
    mail = models.EmailField(max_length=50, unique=True)
    role = models.ForeignKey("Role", on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)  # Champ obligatoire pour Django
    is_staff = models.BooleanField(default=False)  # Pour gérer les permissions

    USERNAME_FIELD = "pseudo"  # Utilisé pour l'authentification
    REQUIRED_FIELDS = ["mail"]  # Champs obligatoires pour createsuperuser

    objects = UserManager()  # Associe le UserManager

    def __str__(self):
        return self.pseudo

# Modèle Theme
class Theme(models.Model):
    titre = models.CharField(max_length=256)

    def __str__(self):
        return self.titre

# Modèle Petition
class Petition(models.Model):
    titre = models.CharField(max_length=256)
    description = models.TextField(max_length=1024)
    image_url = models.TextField(max_length=1024, null=True)
    date_creation = models.DateField()
    date_cloture = models.DateField()
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

# Modèle Signer (Table de relation Many-to-Many entre Petition et User)
class Signer(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('petition', 'user')  # Clé primaire composite

    def __str__(self):
        return f"{self.user.pseudo} a signé {self.petition.titre}"

# Modèle Messagerie (Table de messages entre User et Petition)
class Messagerie(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_heure = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=256)
    toxicite = models.FloatField(default=0.0)
    insulte = models.FloatField(default=0.0)
    haine = models.FloatField(default=0.0)
    menace = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('petition', 'user', 'date_heure') 
    def __str__(self):
        return f"Message de {self.user.pseudo} sur {self.petition.titre}"
