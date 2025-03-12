from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Petition
from app.serializers import PetitionSerializer
from rest_framework.permissions import IsAuthenticated

from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from app.models import Petition, User, Theme

class CreatePetitionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        titre = request.data.get("titre")
        description = request.data.get("description")
        date_creation = datetime.now().date()
        date_cloture = request.data.get("date_cloture")
        user_id = request.data.get("user_id")
        # theme_id = request.data.get("theme")
        
        # Vérifier si la pétition existe déjà
        if Petition.objects.filter(titre=titre).exists():
            return Response({"error": "Cette pétition existe déjà"}, status=status.HTTP_400_BAD_REQUEST)

        # Récupérer l'utilisateur (ou renvoyer une erreur si l'ID est incorrect)
        user = get_object_or_404(User, id=user_id)

        # Récupérer le thème (ou renvoyer une erreur si l'ID est incorrect)
        theme = get_object_or_404(Theme, id=5)

        # Créer la pétition avec les relations User et Theme
        petition = Petition.objects.create(
            titre=titre,
            description=description,
            date_creation=date_creation,
            date_cloture=date_cloture,
            user=user,
            theme=theme
        )

        return Response(
            {"message": "Pétition créée avec succès, partagez-la !", "petition": PetitionSerializer(petition).data},
            status=status.HTTP_201_CREATED
        )

class ListPetitionAPIView(APIView):
    def get(self, request):
        petitions = Petition.objects.all()
        serializer = PetitionSerializer(petitions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PetitionAPIView(APIView):
    def get(self, request, petition_id):  # Ajoute `petition_id` en argument
        petition = get_object_or_404(Petition, id=petition_id)
        serializer = PetitionSerializer(petition)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ListPetitionByNameAPIView(APIView):
    def get(self, request, petition_name):
        petitions = Petition.objects.filter(titre__icontains=petition_name)[:15]
        serializer = PetitionSerializer(petitions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


