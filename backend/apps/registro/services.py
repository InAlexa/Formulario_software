import jwt
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction

from .models import Perfil


@transaction.atomic
def crear_usuario(validated_data):
    """
    Crea el User de Django (contraseña con hash nativo) + su Perfil,
    y dispara el correo de verificación a través de Supabase.
    """
    user = User.objects.create_user(
        username=validated_data["correo"],
        email=validated_data["correo"],
        first_name=validated_data["nombre"],
        last_name=validated_data["apellido"],
        password=validated_data["contrasena"],
        is_active=False,  # se activa cuando se verifica el correo
    )
    perfil = Perfil.objects.create(user=user, edad=validated_data["edad"])

    enviar_verificacion_supabase(user.email)

    return perfil


def enviar_verificacion_supabase(correo):
    """
    Le pide a Supabase que envíe el correo de verificación (magic link / OTP).
    Supabase solo se usa como "cartero" de la verificación: no guardamos
    ni sincronizamos la contraseña con él.
    """
    url = f"{settings.SUPABASE_URL}/auth/v1/otp"
    headers = {
        "apikey": settings.SUPABASE_ANON_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "email": correo,
        "create_user": True,
        "options": {
            "email_redirect_to": settings.SUPABASE_EMAIL_REDIRECT_URL,
        },
    }
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    return response


def confirmar_verificacion(access_token):
    """
    Valida el JWT que Supabase entrega al frontend tras confirmar el
    correo, y si es válido, activa al usuario en Django.
    """
    try:
        payload = jwt.decode(
            access_token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except jwt.PyJWTError as exc:
        raise ValueError("Token de verificación inválido o expirado.") from exc

    correo = payload.get("email")
    if not correo:
        raise ValueError("El token no contiene un correo válido.")

    try:
        user = User.objects.select_related("perfil").get(email__iexact=correo)
    except User.DoesNotExist as exc:
        raise ValueError("No existe una cuenta asociada a este correo.") from exc

    user.is_active = True
    user.save(update_fields=["is_active"])

    perfil = user.perfil
    perfil.correo_verificado = True
    perfil.save(update_fields=["correo_verificado"])

    return perfil
