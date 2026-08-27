from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from rest_framework import serializers

from .models import Perfil


class RegistroSerializer(serializers.Serializer):
    """
    Serializador de entrada/salida para el registro.
    Los nombres de los campos se mantienen en sincronía
    con el frontend (nombre, apellido, edad, correo, contrasena).
    """

    nombre = serializers.CharField(max_length=150)
    apellido = serializers.CharField(max_length=150)
    edad = serializers.IntegerField(validators=[MinValueValidator(18)])
    correo = serializers.EmailField()
    contrasena = serializers.CharField(write_only=True, min_length=8)

    def validate_correo(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Ya existe una cuenta con este correo.")
        return value

    def create(self, validated_data):
        # La lógica real de creación vive en services.py;
        # este método solo delega para mantener el serializer simple.
        from .services import crear_usuario

        return crear_usuario(validated_data)

    def to_representation(self, instance):
        # instance aquí es el objeto Perfil devuelto por crear_usuario()
        user = instance.user
        return {
            "id": user.id,
            "nombre": user.first_name,
            "apellido": user.last_name,
            "edad": instance.edad,
            "correo": user.email,
            "correo_verificado": instance.correo_verificado,
        }


class VerificarCorreoSerializer(serializers.Serializer):
    """
    Recibe el access_token que Supabase entrega al frontend
    cuando el usuario confirma su correo.
    """

    access_token = serializers.CharField()
