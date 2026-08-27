import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api";

const registroApi = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

export const postRegistro = (datos) => registroApi.post("/registro/", datos);

export const postVerificarCorreo = (accessToken) =>
  registroApi.post("/registro/verificar/", { access_token: accessToken });

export default registroApi;
