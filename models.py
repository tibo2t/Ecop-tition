from django.db import models

# Modèle Role
class Role(models.Model):
    nom_role = models.CharField(max_length=50)

    def __str__(self):
        return self.nom_role

# Modèle User
class User(models.Model):
    pseudo = models.CharField(max_length=50, unique=True)
    mail = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=256)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

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

    class Meta:
        unique_together = ('petition', 'user', 'date_heure')  # Clé primaire composite

    def __str__(self):
        return f"Message de {self.user.pseudo} sur {self.petition.titre}"
