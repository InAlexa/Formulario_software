import { postRegistro, postVerificarCorreo } from "../api/registroApi";

// 1. Crea el usuario en Django (contraseña hasheada, is_active=False)
export const registrarUsuario = async (datos) => {
  const response = await postRegistro(datos);
  return response.data;
};

// 2. Confirma en Django el token que Supabase entregó tras verificar el correo
export const confirmarCorreo = async (accessToken) => {
  const response = await postVerificarCorreo(accessToken);
  return response.data;
};
