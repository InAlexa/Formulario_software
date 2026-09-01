import re

from django.core.exceptions import ValidationError

SOLO_LETRAS_REGEX = re.compile(r"^[A-Za-zÀ-ÿ\s]+$")
MAYUSCULA_REGEX = re.compile(r"[A-Z]")
NUMERO_REGEX = re.compile(r"[0-9]")

# Regla 1: nombre y apellido solo deben aceptar letras (nada de números ni símbolos).
# Regla 2: contraseña debe tener al menos una mayúscula y un número (además del mínimo de 8 caracteres que ya existía).

def validar_solo_letras(value):
    if not SOLO_LETRAS_REGEX.match(value.strip()):
        raise ValidationError("Solo se permiten letras.")


def validar_contrasena_compleja(value):
    if not MAYUSCULA_REGEX.search(value) or not NUMERO_REGEX.search(value):
        raise ValidationError(
            "La contraseña debe tener al menos una mayúscula y un número."
        )