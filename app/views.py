import bcrypt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Role
from .serializers import UserSerializer

class RegisterAPIView(APIView):
    def post(self, request):
        pseudo = request.data.get("pseudo")
        mail = request.data.get("mail")
        password = request.data.get("password")
        id_role = request.data.get("id_role") 

        if User.objects.filter(pseudo=pseudo).exists():
            return Response({"error": "Pseudo déjà utilisé"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(mail=mail).exists():
            return Response({"error": "Mail déjà utilisé"}, status=status.HTTP_400_BAD_REQUEST)

        # Hash du mot de passe avec bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Vérifier si le rôle existe, sinon mettre un rôle par défaut (ex: ID = 1)
        role = Role.objects.get(id=id_role) if Role.objects.filter(id=id_role).exists() else Role.objects.first()

        # Création de l'utilisateur
        user = User.objects.create(
            pseudo=pseudo,
            mail=mail,
            password=hashed_password,
            role=role
        )

        return Response({"message": "Compte créé avec succès", "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
