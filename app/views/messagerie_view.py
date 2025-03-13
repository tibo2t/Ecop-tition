from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Messagerie, Petition
from app.serializers import MessagerieSerializer
from rest_framework.permissions import IsAuthenticated

class CreateMessagerieAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        petition_id = request.data.get("petition_id")
        message = request.data.get("message")

        if not petition_id or not message:
            return Response({"error": "petition_id et message sont requis"}, status=status.HTTP_400_BAD_REQUEST)
       
        try:
            petition = Petition.objects.get(pk=int(petition_id))  # Convertir en entier ici
        except (Petition.DoesNotExist, ValueError):
            return Response({"error": "La pétition spécifiée n'existe pas ou ID invalide"}, status=status.HTTP_404_NOT_FOUND)

        # Création du message
        messagerie = Messagerie.objects.create(
            petition=petition,
            user=request.user,  # Django récupère l'utilisateur connecté
            message=message,
            toxicite=0.0,
            insulte=0.0,
            haine=0.0,
            menace=0.0
        )
        return Response({"message": "Message créé avec succès", "messagerie": MessagerieSerializer(messagerie).data}, status=status.HTTP_201_CREATED)

class ListMessageriesAPIView(APIView):
    def get(self, request):
        messageries = Messagerie.objects.all()
        serializer = MessagerieSerializer(messageries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteMessagerieAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, messagerie_id):
        try:
            messagerie = Messagerie.objects.get(id=messagerie_id)
            messagerie.delete()
            return Response({"message": "Message supprimé avec succès"}, status=status.HTTP_200_OK)
        except Messagerie.DoesNotExist:
            return Response({"error": "Message non trouvé"}, status=status.HTTP_404_NOT_FOUND)
