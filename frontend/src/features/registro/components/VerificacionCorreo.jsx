import { useVerificacionCorreo } from "../hooks/useVerificacionCorreo";

const VerificacionCorreo = () => {
  const { loading, error, correo } = useVerificacionCorreo();

  if (loading) return <p>Verificando tu correo...</p>;
  if (error) return <p style={{ color: "#c0392b" }}>{error}</p>;

  return (
    <p style={{ color: "#1e8449" }}>
      ¡Correo {correo} verificado! Ya puedes iniciar sesión.
    </p>
  );
};

export default VerificacionCorreo;
