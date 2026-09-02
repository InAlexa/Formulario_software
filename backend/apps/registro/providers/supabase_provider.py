import jwt
import requests
from django.conf import settings
from jwt import PyJWKClient

from .base import EmailVerificationProvider


class SupabaseEmailProvider(EmailVerificationProvider):
    def __init__(self):
        self._jwks_client = None

    def enviar_verificacion(self, correo):
        url = f"{settings.SUPABASE_URL}/auth/v1/otp"
        headers = {
            "apikey": settings.SUPABASE_ANON_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "email": correo,
            "create_user": True,
            "options": {"email_redirect_to": settings.SUPABASE_EMAIL_REDIRECT_URL},
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            if response.status_code == 429:
                raise ValueError(
                    "Supabase limitó el envío de correos por ahora. "
                    "Espera unos minutos o usa otro correo para probar."
                ) from exc
            raise ValueError(
                "No se pudo enviar el correo de verificación."
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise ValueError(
                "No se pudo contactar el servicio de verificación de correo."
            ) from exc

    def _get_jwks_client(self):
        if self._jwks_client is None:
            jwks_url = f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"
            self._jwks_client = PyJWKClient(jwks_url)
        return self._jwks_client

    def confirmar_token(self, token):
        try:
            signing_key = self._get_jwks_client().get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token, signing_key.key, algorithms=["ES256"], audience="authenticated"
            )
        except jwt.PyJWTError as exc:
            raise ValueError("Token de verificación inválido o expirado.") from exc

        correo = payload.get("email")
        if not correo:
            raise ValueError("El token no contiene un correo válido.")
        return correo