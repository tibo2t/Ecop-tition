from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.models import Theme
from app.serializers import ThemeSerializer


class CreateThemeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Créer un nouveau thème.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["titre"],
            properties={
                "titre": openapi.Schema(type=openapi.TYPE_STRING, description="Nom du thème"),
            },
        ),
        responses={
            201: openapi.Response("Thème créé avec succès", ThemeSerializer),
            400: openapi.Response("Ce thème existe déjà"),
            403: openapi.Response("Authentification requise"),
        },
    )
    def post(self, request):
        """Créer un thème."""
        titre = request.data.get("titre")
        if Theme.objects.filter(titre=titre).exists():
            return Response({"error": "Ce thème existe déjà"}, status=status.HTTP_400_BAD_REQUEST)

        theme = Theme.objects.create(titre=titre)
        return Response({"message": "Thème créé avec succès", "theme": ThemeSerializer(theme).data}, status=status.HTTP_201_CREATED)


class ListThemesAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Récupérer la liste de tous les thèmes.",
        responses={
            200: openapi.Response("Liste des thèmes", ThemeSerializer(many=True)),
        },
    )
    def get(self, request):
        """Lister tous les thèmes."""
        themes = Theme.objects.all()
        serializer = ThemeSerializer(themes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteThemeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Supprimer un thème spécifique.",
        manual_parameters=[
            openapi.Parameter(
                "theme_id",
                openapi.IN_PATH,
                description="ID du thème à supprimer",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            200: openapi.Response("Thème supprimé avec succès"),
            404: openapi.Response("Thème non trouvé"),
            403: openapi.Response("Authentification requise"),
        },
    )
    def delete(self, request, theme_id):
        """Supprimer un thème par ID."""
        try:
            theme = Theme.objects.get(id=theme_id)
            theme.delete()
            return Response({"message": "Thème supprimé avec succès"}, status=status.HTTP_200_OK)
        except Theme.DoesNotExist:
            return Response({"error": "Thème non trouvé"}, status=status.HTTP_404_NOT_FOUND)
