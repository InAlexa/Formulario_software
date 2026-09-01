# Backend — cómo funciona y cómo conecta con Supabase

## Idea central

Django es el **dueño de los datos**: guarda el usuario, la contraseña
(hasheada) y el perfil en PostgreSQL. Supabase **no** guarda nada que
tu backend necesite — solo se usa como servicio externo para **enviar**
y **firmar** el correo de verificación. Esto evita tener dos sistemas
compitiendo por ser "la fuente de verdad" del usuario.

```
Usuario (form) → Django (crea cuenta, pide a Supabase que mande el correo)
                        ↓
                  Supabase Auth (envía el correo, firma un JWT)
                        ↓
Usuario hace click en el correo → Frontend recibe el JWT en la URL
                        ↓
Frontend manda el JWT a Django → Django lo valida y activa la cuenta
```

## Los 5 archivos de `apps/registro/` y su responsabilidad

| Archivo | Qué hace |
|---|---|
| `models.py` | Define `Perfil`, extensión 1-a-1 del `User` de Django. Guarda `edad` y `correo_verificado`. |
| `serializers.py` | Valida el JSON que llega del frontend (`nombre`, `apellido`, `edad`, `correo`, `contrasena`) y define cómo se ve la respuesta. No contiene lógica de negocio. |
| `services.py` | Toda la lógica real: crear el `User`+`Perfil`, hablar con la API de Supabase, y validar el JWT cuando el usuario confirma. |
| `views.py` | Solo recibe la petición HTTP, delega a `services.py`, y devuelve la respuesta. Deliberadamente "tonta". |
| `urls.py` | Conecta las dos rutas (`/api/registro/` y `/api/registro/verificar/`) con sus vistas. |

Esta separación (view → service → model) es la misma que usan en
`Blessing` y los demás proyectos: las vistas nunca deben saber *cómo*
se hace algo, solo *a quién pedírselo*.

## Paso a paso del flujo completo

### 1. Registro (`POST /api/registro/`)

1. `RegistroSerializer` valida los 5 campos (incluye que el correo no
   exista ya, y que la edad sea ≥18).
2. `serializer.save()` llama a `services.crear_usuario()`, que:
   - Crea el `User` de Django con `is_active=False` y la contraseña
     hasheada (`create_user` hace el hash automáticamente, nunca se
     guarda en texto plano).
   - Crea el `Perfil` asociado con la `edad`.
   - Llama a `enviar_verificacion_supabase(correo)`.
3. `enviar_verificacion_supabase()` hace un `POST` a
   `https://<tu-proyecto>.supabase.co/auth/v1/otp` usando tu
   `SUPABASE_ANON_KEY` (la "Publishable key" del dashboard). Esto le
   dice a Supabase: "mándale un link de verificación a este correo".
   Supabase se encarga de la plantilla del correo y del envío — Django
   nunca toca un servidor SMTP directamente.

### 2. El usuario confirma su correo

Supabase manda el correo con un link que, al hacer click, redirige al
`SUPABASE_EMAIL_REDIRECT_URL` que configuraste (ej.
`http://localhost:5173/verificado`) con un `access_token` (JWT) pegado
en la URL. Ese JWT lo firma Supabase con tu `SUPABASE_JWT_SECRET`.

### 3. Confirmación (`POST /api/registro/verificar/`)

1. El frontend toma ese `access_token` de la URL y lo manda a Django.
2. `services.confirmar_verificacion()` usa `PyJWT` para **decodificar y
   validar la firma** del token con `SUPABASE_JWT_SECRET`. Si la firma
   no coincide o el token expiró, se rechaza (`400`).
3. Si el token es válido, se extrae el `email` del payload, se busca
   el `User` correspondiente, se pone `is_active=True`, y su `Perfil`
   pasa a `correo_verificado=True`.

## Por qué el JWT es la parte importante

Django **nunca le pregunta a Supabase** "¿este usuario ya se verificó?".
En vez de eso, confía en la firma criptográfica del JWT: si el token
fue firmado con tu `SUPABASE_JWT_SECRET`, solo Supabase pudo haberlo
generado, así que Django puede confiar en su contenido sin hacer una
llamada de red adicional. Esto es más rápido y no depende de que
Supabase esté disponible en el momento de la confirmación.

## Variables de entorno que usa el backend

```
SUPABASE_URL                 → a qué proyecto de Supabase le hablamos
SUPABASE_ANON_KEY            → autoriza la llamada que manda el correo
SUPABASE_JWT_SECRET          → valida la firma del token de verificación
SUPABASE_EMAIL_REDIRECT_URL  → a dónde manda Supabase al usuario tras confirmar
```

Ninguna de estas expone datos sensibles del usuario: la `ANON_KEY` es
pública por diseño (así la trata Supabase), y el `JWT_SECRET` solo vive
en el backend — nunca en el frontend.
