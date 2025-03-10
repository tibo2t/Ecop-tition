from rest_framework import serializers
from .models import Role, User, Theme, Petition, Signer, Messagerie

# Serializer pour le modèle Role
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'  # Inclut tous les champs du modèle

# Serializer pour le modèle User
class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)  # Inclut les détails du rôle

    class Meta:
        model = User
        fields = ['id', 'pseudo', 'mail', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}  # Cache le mot de passe

# Serializer pour le modèle Theme
class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'

# Serializer pour le modèle Petition
class PetitionSerializer(serializers.ModelSerializer):
    theme = ThemeSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Petition
        fields = '__all__'

# Serializer pour la relation Signer (Many-to-Many)
class SignerSerializer(serializers.ModelSerializer):
    petition = PetitionSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Signer
        fields = '__all__'

# Serializer pour le modèle Messagerie
class MessagerieSerializer(serializers.ModelSerializer):
    petition = PetitionSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Messagerie
        fields = '__all__'
