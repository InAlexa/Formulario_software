import { useEffect, useState } from "react";

import { confirmarCorreo } from "../service/registroService";

const obtenerAccessToken = () => {
  const hash = window.location.hash.replace("#", "");
  const params = new URLSearchParams(hash);
  return params.get("access_token");
};

export const useVerificacionCorreo = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [correo, setCorreo] = useState(null);

  useEffect(() => {
    const verificar = async () => {
      const accessToken = obtenerAccessToken();

      if (!accessToken) {
        setError("No se encontró un token de verificación en el enlace.");
        setLoading(false);
        return;
      }

      try {
        const data = await confirmarCorreo(accessToken);
        setCorreo(data.correo);
      } catch (err) {
        setError(
          err.response?.data?.detail ?? "No se pudo verificar el correo.",
        );
      } finally {
        setLoading(false);
      }
    };

    verificar();
  }, []);

  return { loading, error, correo };
};
