import { useEffect, useState } from "react";

import { confirmarCorreo } from "../service/registroService";

const obtenerToken = () => {
  const paramsQuery = new URLSearchParams(window.location.search);
  if (paramsQuery.get("token")) return paramsQuery.get("token");

  const hash = window.location.hash.replace("#", "");
  return new URLSearchParams(hash).get("access_token");
};

export const useVerificacionCorreo = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [correo, setCorreo] = useState(null);

  useEffect(() => {
    const verificar = async () => {
      const accessToken = obtenerToken();

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
