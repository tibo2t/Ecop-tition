"""Ecopétition URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views.auth_views import RegisterAPIView, LoginView, VerifyTokenAPIView
from app.views.themes_views import CreateThemeAPIView, ListThemesAPIView, DeleteThemeAPIView
from app.views.messagerie_view import CreateMessagerieAPIView, ListMessageriesAPIView, DeleteMessagerieAPIView
from app.views.sign_views import SignPetitionAPIView, PetitionSignatureCountAPIView
from app.views.petitions_view import CreatePetitionAPIView, ListPetitionAPIView, PetitionAPIView, PaginatedListPetitionAPIView, ListPetitionByNameAPIView
from app.views.messagerie_views import PetitionCommentsAPIView
from app.views.user_view import CheckIfUserHasSignOnePetitionAPIView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from app.permissions import AllowAnyForSwagger  # Import de la permission

schema_view = get_schema_view(
    openapi.Info(
        title="API Ecopétition",
        default_version='v1',
        description="Documentation interactive des endpoints de l'API",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(AllowAnyForSwagger,),  # Applique la permission personnalisée
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentification
    path('api/user/register', RegisterAPIView.as_view(), name='register'),
    path('api/user/login', LoginView.as_view(), name='login'),
    path('api/user/verify', VerifyTokenAPIView.as_view(), name='verify-token'),

    # User
    path('api/user/check_if_has_sign_petition/<int:user_id>',CheckIfUserHasSignOnePetitionAPIView.as_view(), name='check_if_has_sign_petition'),

    # Thèmes
    path('api/themes/create', CreateThemeAPIView.as_view(), name='create_theme'),
    path('api/themes', ListThemesAPIView.as_view(), name='list_themes'),
    path('api/themes/delete/<int:theme_id>', DeleteThemeAPIView.as_view(), name='delete_theme'),

    # Messagerie
    path('api/messagerie', ListMessageriesAPIView.as_view(), name='list_messageries'), 
    path('api/messagerie/create', CreateMessagerieAPIView.as_view(), name='create_messagerie'), 
    path('api/messagerie/<int:messagerie_id>/delete', DeleteMessagerieAPIView.as_view(), name='delete_messagerie'),
    path('api/petitions/<int:petition_id>/comments/', PetitionCommentsAPIView.as_view(), name='petition_comments'),

    # Pétitions
    path('api/petitions', ListPetitionAPIView.as_view(), name='list_petitions'),
    path('api/petitions/create', CreatePetitionAPIView.as_view(), name='create_petition'),
    path('api/petitions/<int:petition_id>', PetitionAPIView.as_view(), name='petition'),
    path('api/petitions/search/<str:petition_name>', ListPetitionByNameAPIView.as_view(), name='list_petitions_name'),
    path('api/petitions/list/paginated', PaginatedListPetitionAPIView.as_view(), name='paginated-petitions'),
    path('api/petitions/<int:petition_id>/sign', SignPetitionAPIView.as_view(), name="sign-petition"),
    path('api/petitions/<int:petition_id>/sign_count', PetitionSignatureCountAPIView.as_view(), name='petition_signature_count'),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
