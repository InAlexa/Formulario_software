from abc import ABC, abstractmethod


class EmailVerificationProvider(ABC):
    """
    Contrato que cualquier proveedor de verificación de correo debe
    cumplir. views.py y services.py solo conocen esta interfaz —
    nunca saben si por debajo hay Supabase, Resend, o lo que sea.
    """

    @abstractmethod
    def enviar_verificacion(self, correo: str) -> None:
        """Envía el correo con el link/código de verificación."""
        raise NotImplementedError

    @abstractmethod
    def confirmar_token(self, token: str) -> str:
        """
        Valida el token recibido y devuelve el correo verificado.
        Lanza ValueError si el token es inválido o expiró.
        """
        raise NotImplementedError