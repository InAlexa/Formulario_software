from django.contrib.auth.models import User
from django.db import transaction

from .models import Perfil
from .providers import get_email_provider


@transaction.atomic
def crear_usuario(validated_data):
    user = User.objects.create_user(
        username=validated_data["correo"],
        email=validated_data["correo"],
        first_name=validated_data["nombre"],
        last_name=validated_data["apellido"],
        password=validated_data["contrasena"],
        is_active=False,
    )
    perfil = Perfil.objects.create(user=user, edad=validated_data["edad"])

    get_email_provider().enviar_verificacion(user.email)

    return perfil


def confirmar_verificacion(token):
    correo = get_email_provider().confirmar_token(token)

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