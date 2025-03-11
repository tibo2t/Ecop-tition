from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Petition, Signer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class SignPetitionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, petition_id):
        try:
            # Vérifier si la pétition existe
            petition = Petition.objects.get(id=petition_id)
        except Petition.DoesNotExist:
            return Response({"error": "Pétition non trouvée"}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si l'utilisateur a déjà signé la pétition
        if Signer.objects.filter(petition=petition, user=request.user).exists():
            return Response({"error": "Vous avez déjà signé cette pétition"}, status=status.HTTP_400_BAD_REQUEST)

        # Enregistrer la signature
        Signer.objects.create(petition=petition, user=request.user)
        
        return Response({"message": "Pétition signée avec succès"}, status=status.HTTP_201_CREATED)
