from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        errors = {}

        # Correo
        email = data.get("email", "").strip()

        if not email:
            errors["email"] = "El correo es requerido"
        elif "@" not in email:
            errors["email"] = "El correo no es válido"
        elif User.objects.filter(email=email).exists():
            errors["email"] = "Este correo ya está registrado"

        # Nombre
        first_name = data.get("first_name", "").strip()

        if not first_name:
            errors["first_name"] = "El nombre es requerido"

        # Apellidos
        last_name = data.get("last_name", "").strip()

        if not last_name:
            errors["last_name"] = "Los apellidos son requeridos"

        # Edad
        age = data.get("age")

        if age in (None, ""):
            errors["age"] = "La edad es requerida"
        else:
            try:
                age = int(age)

                if age < 1:
                    errors["age"] = "La edad debe ser mayor que 0"

                elif age > 120:
                    errors["age"] = "La edad no es válida"

            except (ValueError, TypeError):
                errors["age"] = "La edad debe ser un número"

        # Contraseña
        password = data.get("password", "")

        if not password:
            errors["password"] = "La contraseña es requerida"

        elif len(password) < 8:
            errors["password"] = (
                "La contraseña debe tener al menos 8 caracteres"
            )

        # Si existen errores
        if errors:
            return Response(
                {"errors": errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Si todo está correcto
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )