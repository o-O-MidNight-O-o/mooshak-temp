from rest_framework.exceptions import AuthenticationFailed

def get_token_payload(request):
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        raise AuthenticationFailed("Authorization header must be 'Bearer <token>'")

    token = auth_header.split(' ')[1]

    try:
        payload = decode_token(token)
    except Exception:
        raise AuthenticationFailed("Invalid or expired token")

    return payload


# Optional example for JWT
import jwt
from django.conf import settings

def decode_token(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
