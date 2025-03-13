from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from app.models import Signer, User, Petition


class CheckIfUserHasSignOnePetitionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, petition_id):
        petition = get_object_or_404(Petition, id=petition_id)
        user = request.user
        has_signed = Signer.objects.filter(petition=petition, user=user).exists()

        return Response({"has_signed": has_signed})

