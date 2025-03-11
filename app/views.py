import bcrypt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Role
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .views.auth_views import RegisterAPIView, LoginView

