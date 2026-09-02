import requests
from django.conf import settings
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner

from .base import EmailVerificationProvider

_signer = TimestampSigner()
TOKEN_MAX_AGE_SEGUNDOS = 60 * 60  # 1 hora


class ResendEmailProvider(EmailVerificationProvider):
    def enviar_verificacion(self, correo):
        token = _signer.sign(correo)
        link = f"{settings.EMAIL_VERIFICATION_REDIRECT_URL}?token={token}"

        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "from": settings.RESEND_FROM_EMAIL,
            "to": [correo],
            "subject": "Confirma tu correo",
            "html": f"<p>Haz click para verificar tu cuenta:</p><p><a href='{link}'>{link}</a></p>",
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise ValueError(
                "No se pudo enviar el correo de verificación con Resend."
            ) from exc

    def confirmar_token(self, token):
        try:
            correo = _signer.unsign(token, max_age=TOKEN_MAX_AGE_SEGUNDOS)
        except SignatureExpired as exc:
            raise ValueError("El link de verificación ya expiró.") from exc
        except BadSignature as exc:
            raise ValueError("Token de verificación inválido.") from exc
        return correo