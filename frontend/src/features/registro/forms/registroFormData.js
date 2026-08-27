export const registroFormInicial = {
  nombre: "",
  apellido: "",
  edad: "",
  correo: "",
  contrasena: "",
};

const CORREO_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export const validarRegistroForm = (valores) => {
  const errores = {};

  if (!valores.nombre.trim()) {
    errores.nombre = "El nombre es obligatorio.";
  }

  if (!valores.apellido.trim()) {
    errores.apellido = "El apellido es obligatorio.";
  }

  if (!valores.edad) {
    errores.edad = "La edad es obligatoria.";
  } else if (Number(valores.edad) < 18) {
    errores.edad = "Debes ser mayor de 18 años.";
  }

  if (!valores.correo.trim()) {
    errores.correo = "El correo es obligatorio.";
  } else if (!CORREO_REGEX.test(valores.correo)) {
    errores.correo = "El correo no tiene un formato válido.";
  }

  if (!valores.contrasena) {
    errores.contrasena = "La contraseña es obligatoria.";
  } else if (valores.contrasena.length < 8) {
    errores.contrasena = "La contraseña debe tener al menos 8 caracteres.";
  }

  return errores;
};
