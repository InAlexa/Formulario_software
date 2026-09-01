import { useState } from "react";

import { registrarUsuario } from "../service/registroService";
import {
  registroFormInicial,
  validarRegistroForm,
} from "../forms/registroFormData";

export const useRegistro = () => {
  const [valores, setValores] = useState(registroFormInicial);
  const [erroresForm, setErroresForm] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [registroExitoso, setRegistroExitoso] = useState(false);

  const handleChange = (evento) => {
    const { name, value } = evento.target;
    setValores((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (evento) => {
    evento.preventDefault();
    setError(null);
    setRegistroExitoso(false);

    const errores = validarRegistroForm(valores);
    setErroresForm(errores);
    if (Object.keys(errores).length > 0) return;

    setLoading(true);
    try {
      await registrarUsuario({
        ...valores,
        edad: Number(valores.edad),
      });
      setRegistroExitoso(true);
      setValores(registroFormInicial);
    } catch (err) {
      const mensaje =
        err.response?.data?.detail ??
        err.response?.data?.correo?.[0] ??
        "Ocurrió un error al registrar. Intenta de nuevo.";
      setError(mensaje);
    } finally {
      setLoading(false);
    }
  };

  return {
    valores,
    erroresForm,
    loading,
    error,
    registroExitoso,
    handleChange,
    handleSubmit,
  };
};
