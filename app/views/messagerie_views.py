from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Petition, Messagerie
from ..serializers import MessagerieSerializer

class PetitionCommentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, petition_id):
        try:
            # Vérifier si la pétition existe
            petition = Petition.objects.get(id=petition_id)
        except Petition.DoesNotExist:
            return Response({"error": "Pétition non trouvée"}, status=status.HTTP_404_NOT_FOUND)

        # Récupérer tous les messages associés à cette pétition
        messages = Messagerie.objects.filter(petition=petition).order_by("-date_heure")

        # Sérialiser les messages
        serializer = MessagerieSerializer(messages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
