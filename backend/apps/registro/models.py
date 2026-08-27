from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Perfil(models.Model):
    """
    Extiende al User nativo de Django con los campos que
    necesitamos para el registro (edad) y el estado de
    verificación de correo manejado a través de Supabase.

    nombre    -> user.first_name
    apellido  -> user.last_name
    correo    -> user.email
    contrasena -> user.password (hash nativo de Django)
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    edad = models.PositiveIntegerField(
        validators=[MinValueValidator(18, message="Debes ser mayor de 18 años.")]
    )
    correo_verificado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Perfil de {self.user.email}"
