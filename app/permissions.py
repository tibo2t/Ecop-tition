from rest_framework.permissions import BasePermission

class AllowAnyForSwagger(BasePermission):
    """
    Autorise tout le monde à accéder à Swagger et Redoc, 
    mais applique les restrictions normales ailleurs.
    """
    def has_permission(self, request, view):
        return request.resolver_match.url_name in ['schema-swagger-ui', 'schema-redoc']
