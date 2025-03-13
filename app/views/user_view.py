from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from app.models import Signer, User


class CheckIfUserHasSignOnePetitionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        has_signed = Signer.objects.filter(user=user).exists()

        return Response({"has_signed": has_signed})

