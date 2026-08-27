import { createClient } from "@supabase/supabase-js";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

// Nota: Supabase aquí NO es la fuente de verdad del usuario.
// Django guarda los datos y la contraseña; Supabase solo se usa
// para el flujo de verificación de correo (OTP / magic link).
export const supabase = createClient(supabaseUrl, supabaseAnonKey);
