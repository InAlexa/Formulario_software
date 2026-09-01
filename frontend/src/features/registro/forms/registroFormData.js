export const registroFormInicial = {
  nombre: "",
  apellido: "",
  edad: "",
  correo: "",
  contrasena: "",
};

const SOLO_LETRAS_REGEX = /^[A-Za-zÀ-ÿ\s]+$/;
const CORREO_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const MAYUSCULA_REGEX = /[A-Z]/;
const NUMERO_REGEX = /[0-9]/;

// Cada campo es una lista de reglas. Agregar una regla nueva es
// sumar una entrada aquí, sin tocar las reglas que ya existen.
const reglasPorCampo = {
  nombre: [
    { test: (v) => v.trim().length > 0, mensaje: "El nombre es obligatorio." },
    {
      test: (v) => SOLO_LETRAS_REGEX.test(v.trim()),
      mensaje: "El nombre solo puede contener letras.",
    },
  ],
  apellido: [
    {
      test: (v) => v.trim().length > 0,
      mensaje: "El apellido es obligatorio.",
    },
    {
      test: (v) => SOLO_LETRAS_REGEX.test(v.trim()),
      mensaje: "El apellido solo puede contener letras.",
    },
  ],
  edad: [
    { test: (v) => v !== "", mensaje: "La edad es obligatoria." },
    { test: (v) => Number(v) >= 18, mensaje: "Debes ser mayor de 18 años." },
  ],
  correo: [
    { test: (v) => v.trim().length > 0, mensaje: "El correo es obligatorio." },
    {
      test: (v) => CORREO_REGEX.test(v),
      mensaje: "El correo no tiene un formato válido.",
    },
  ],
  contrasena: [
    { test: (v) => v.length > 0, mensaje: "La contraseña es obligatoria." },
    {
      test: (v) => v.length >= 8,
      mensaje: "La contraseña debe tener al menos 8 caracteres.",
    },
    {
      test: (v) => MAYUSCULA_REGEX.test(v),
      mensaje: "La contraseña debe tener al menos una mayúscula.",
    },
    {
      test: (v) => NUMERO_REGEX.test(v),
      mensaje: "La contraseña debe tener al menos un número.",
    },
  ],
};
// Regla 1: nombre y apellido solo deben aceptar letras (nada de números ni símbolos).
// Regla 2: contraseña debe tener al menos una mayúscula y un número (además del mínimo de 8 caracteres que ya existía).

export const validarRegistroForm = (valores) => {
  const errores = {};

  for (const campo of Object.keys(reglasPorCampo)) {
    for (const regla of reglasPorCampo[campo]) {
      if (!regla.test(valores[campo])) {
        errores[campo] = regla.mensaje;
        break;
      }
    }
  }

  return errores;
};
