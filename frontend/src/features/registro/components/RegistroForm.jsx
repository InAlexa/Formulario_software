import { useRegistro } from "../hooks/useRegistro";
import "./RegistroForm.css";

const RegistroForm = () => {
  const {
    valores,
    erroresForm,
    loading,
    error,
    registroExitoso,
    handleChange,
    handleSubmit,
  } = useRegistro();

  return (
    <div className="registro-contenedor">
      <form className="registro-form" onSubmit={handleSubmit} noValidate>
        <h2>Crear cuenta</h2>

        <div className="registro-campo">
          <label htmlFor="nombre">Nombre</label>
          <input
            id="nombre"
            name="nombre"
            type="text"
            value={valores.nombre}
            onChange={handleChange}
          />
          {erroresForm.nombre && <span className="registro-error">{erroresForm.nombre}</span>}
        </div>

        <div className="registro-campo">
          <label htmlFor="apellido">Apellido</label>
          <input
            id="apellido"
            name="apellido"
            type="text"
            value={valores.apellido}
            onChange={handleChange}
          />
          {erroresForm.apellido && (
            <span className="registro-error">{erroresForm.apellido}</span>
          )}
        </div>

        <div className="registro-campo">
          <label htmlFor="edad">Edad</label>
          <input
            id="edad"
            name="edad"
            type="number"
            min="0"
            value={valores.edad}
            onChange={handleChange}
          />
          {erroresForm.edad && <span className="registro-error">{erroresForm.edad}</span>}
        </div>

        <div className="registro-campo">
          <label htmlFor="correo">Correo</label>
          <input
            id="correo"
            name="correo"
            type="email"
            value={valores.correo}
            onChange={handleChange}
          />
          {erroresForm.correo && <span className="registro-error">{erroresForm.correo}</span>}
        </div>

        <div className="registro-campo">
          <label htmlFor="contrasena">Contraseña</label>
          <input
            id="contrasena"
            name="contrasena"
            type="password"
            value={valores.contrasena}
            onChange={handleChange}
          />
          {erroresForm.contrasena && (
            <span className="registro-error">{erroresForm.contrasena}</span>
          )}
        </div>

        {error && <p className="registro-error registro-error-general">{error}</p>}
        {registroExitoso && (
          <p className="registro-exito">
            ¡Cuenta creada! Revisa tu correo para verificar tu cuenta.
          </p>
        )}

        <button type="submit" disabled={loading}>
          {loading ? "Registrando..." : "Registrarme"}
        </button>
      </form>
    </div>
  );
};

export default RegistroForm;
