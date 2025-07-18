# views.py
from Api.k3.helpers.jwt import verify_jwt
from rest_framework.views import APIView
from Api.models import UserLogin
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, Http404, JsonResponse

class ValidateTokenView(APIView):
    def post(self, request):
        token = request.data.get('token')
        try:
            payload = verify_jwt(token)
            user = UserLogin.objects.filter(idUser=payload['idUser'], Rut=payload['rut']).first()
            if not user:
                return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
            
            return Response({'message': 'Token válido', 'user': user.NameUser}, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
class JWTMiddleware:
    """
    Middleware para validar el token JWT en cada solicitud.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Excluir rutas que no necesitan validación (login, registro, etc.)
        excluded_paths = [
            "/admin/"
            "/static/",
        ]

        # Si la ruta está en las excluidas, permitir el acceso sin validar token
        if any(request.path.startswith(path) for path in excluded_paths):
            return self.get_response(request)

        # Obtener el token del header "x-token"
        token = request.headers.get("x-token")

        if not token:
            return JsonResponse({"error": "acceso denegado"}, status=403)

        # Verificar el token
        decoded_token = verify_jwt(token)
        if not decoded_token:
            return JsonResponse({"error": "Invalid or expired token"}, status=403)

        # Adjuntar el token decodificado a la solicitud para su uso en las vistas
        request.user_data = decoded_token  

        return self.get_response(request)
