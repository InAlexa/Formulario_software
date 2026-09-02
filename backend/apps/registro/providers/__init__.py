from django.conf import settings

from .resend_provider import ResendEmailProvider
from .supabase_provider import SupabaseEmailProvider

# Agregar un proveedor nuevo = sumar una entrada aquí.
# Nunca hay que tocar esta función ni los proveedores que ya existen.
_PROVIDERS = {
    "supabase": SupabaseEmailProvider,
    "resend": ResendEmailProvider,
}


def get_email_provider():
    nombre = settings.EMAIL_VERIFICATION_PROVIDER
    clase = _PROVIDERS.get(nombre)
    if clase is None:
        raise ValueError(f"Proveedor de correo desconocido: {nombre}")
    return clase()