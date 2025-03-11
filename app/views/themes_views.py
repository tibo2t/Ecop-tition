from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Theme
from app.serializers import ThemeSerializerom rest_framework.permissions import IsAuthenticated

class CreateThemeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        titre = request.data.get("titre")
        if Theme.objects.filter(titre=titre).exists():
            return Response({"error": "Ce thème existe déjà"}, status=status.HTTP_400_BAD_REQUEST)
        
        theme = Theme.objects.create(titre=titre)
        return Response({"message": "Thème créé avec succès", "theme": ThemeSerializer(theme).data}, status=status.HTTP_201_CREATED)

class ListThemesAPIView(APIView):
    def get(self, request):
        themes = Theme.objects.all()
        serializer = ThemeSerializer(themes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteThemeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, theme_id):
        try:
            theme = Theme.objects.get(id=theme_id)
            theme.delete()
            return Response({"message": "Thème supprimé avec succès"}, status=status.HTTP_200_OK)
        except Theme.DoesNotExist:
            return Response({"error": "Thème non trouvé"}, status=status.HTTP_404_NOT_FOUND)
