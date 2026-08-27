from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistroSerializer, VerificarCorreoSerializer
from .services import confirmar_verificacion


class RegistroView(APIView):
    """POST /api/registro/  -> crea el usuario y dispara el correo de verificación."""

    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        perfil = serializer.save()
        data = RegistroSerializer(perfil).data
        return Response(data, status=status.HTTP_201_CREATED)


class VerificarCorreoView(APIView):
    """POST /api/registro/verificar/  -> confirma el correo usando el token de Supabase."""

    def post(self, request):
        serializer = VerificarCorreoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            perfil = confirmar_verificacion(serializer.validated_data["access_token"])
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"correo": perfil.user.email, "correo_verificado": perfil.correo_verificado},
            status=status.HTTP_200_OK,
        )
