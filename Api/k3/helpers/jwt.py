# jwt_helper.py
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

def generate_jwt_token(user_id, rut):
    """
    Genera un token JWT para el usuario.
    
    :param user_id: El ID del usuario
    :param rut: El RUT del usuario
    :return: Un token JWT como string
    """
    try:
        token = jwt.encode({
            'idUser': user_id,
            'rut': rut,
            'exp': datetime.utcnow() + timedelta(minutes=60)  # Token expira en 60 minutos
        }, settings.SECRET_KEY, algorithm='HS256')
        
        return token
    except Exception as e:
        raise e
    
    
def verify_jwt(token):
    try:
        # Decodifica el token
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return decoded_token  # Retorna el contenido del token si es válido
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('El token ha expirado')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Token inválido')
    
def generate_jwt_token_api(user_id, rut):
    """
    Genera un token JWT para el usuario.
    
    :param user_id: El ID del usuario
    :param rut: El RUT del usuario
    :return: Un token JWT como string
    """
    try:
        token = jwt.encode({
            'idUser': user_id,
            'rut': rut,
            'exp': datetime.utcnow() + timedelta(hours=5)  # Token expira en 60 minutos
        }, settings.SECRET_KEY, algorithm='HS256')
        
        return token
    except Exception as e:
        raise e
    
def generate_jwt_token_non_expiring(user, password):
    """
    Genera un token JWT sin fecha de expiración.
    
    :param user_id: El ID del usuario
    :param rut: El RUT del usuario
    :return: Un token JWT sin expiración
    """
    try:
        token = jwt.encode({
            'user': user,
            'password': password
        }, settings.SECRET_KEY, algorithm='HS256')
        
        return token
    except Exception as e:
        raise e
    
def generate_jwt_token_expiring(user, password):
    """
    Genera un token JWT con expiración de 5 horas.
    
    :param user_id: El ID del usuario
    :param rut: El RUT del usuario
    :return: Un token JWT con expiración
    """
    try:
        token = jwt.encode({
            'user': user,
            'password': password,
            'exp': datetime.utcnow() + timedelta(hours=5)  # Expira en 5 horas
        }, settings.SECRET_KEY, algorithm='HS256')
        
        return token
    except Exception as e:
        raise e
    

