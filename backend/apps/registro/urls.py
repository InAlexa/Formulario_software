from django.urls import path

from .views import RegistroView, VerificarCorreoView

urlpatterns = [
    path("registro/", RegistroView.as_view(), name="registro"),
    path("registro/verificar/", VerificarCorreoView.as_view(), name="registro-verificar"),
]
