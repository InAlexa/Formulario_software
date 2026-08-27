# Proyecto Registro — Formulario de registro

Formulario de registro (nombre, apellido, edad, correo, contraseña) con
verificación de correo vía Supabase.

## Idea general

- **Django** es el dueño de los datos y de la contraseña: usa el `User`
  nativo (`first_name`, `last_name`, `email`, `password`) + un modelo
  `Perfil` (edad, correo_verificado).
- **Supabase** se usa _solo_ como servicio de envío/verificación de
  correo (OTP / magic link). No guarda ni gestiona la contraseña real
  del usuario.

## Backend (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edita .env con tus datos de PostgreSQL y de Supabase

# Crea la base de datos en Postgres antes de migrar, ej:
# createdb registro_db

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Endpoints disponibles:

- `POST /api/registro/` → crea el usuario (`nombre`, `apellido`, `edad`, `correo`, `contrasena`)
- `POST /api/registro/verificar/` → confirma el correo (`access_token` de Supabase)

## Frontend (React + Vite)

```bash
cd frontend
npm install
npm install @supabase/supabase-js axios

cp .env.example .env
# Edita .env con la URL de tu API y tus llaves de Supabase

npm run dev
```

## Configurar Supabase (una sola vez)

1. Crea un proyecto en https://supabase.com.
2. En **Authentication → Providers**, deja habilitado el proveedor de Email.
3. En **Authentication → Email Templates**, puedes personalizar el correo
   de "Confirm signup" / "Magic Link".
4. En **Project Settings → API** copia:
   - `Project URL` → `SUPABASE_URL` (backend) / `VITE_SUPABASE_URL` (frontend)
   - `anon public key` → `SUPABASE_ANON_KEY` (backend) / `VITE_SUPABASE_ANON_KEY` (frontend)
5. En **Project Settings → API → JWT Settings** copia el `JWT Secret` →
   `SUPABASE_JWT_SECRET` (solo backend, nunca lo expongas en el frontend).
6. En **Authentication → URL Configuration**, agrega como _Redirect URL_
   la misma que pusiste en `SUPABASE_EMAIL_REDIRECT_URL` /
   `SUPABASE_EMAIL_REDIRECT_URL` (ej. `http://localhost:5173/verificado`).

## Flujo completo

1. El usuario llena el formulario → `POST /api/registro/` crea el `User`
   (inactivo) y el `Perfil`, y Django le pide a Supabase que envíe el
   correo de verificación.
2. El usuario abre el correo y confirma → Supabase redirige al frontend
   con un `access_token` en la URL.
3. El frontend toma ese token y lo manda a `POST /api/registro/verificar/`.
4. Django valida el token contra `SUPABASE_JWT_SECRET`, activa al
   usuario (`is_active=True`) y marca `correo_verificado=True`.

## Pruebas
<img width="900" height="1600" alt="image" src="https://github.com/user-attachments/assets/1c82cac8-ff2d-44ac-8f8b-c43cfe24728d" />
<img width="590" height="1280" alt="image" src="https://github.com/user-attachments/assets/46463182-93f6-4a19-a292-732cbd89d920" />
<img width="1112" height="557" alt="image" src="https://github.com/user-attachments/assets/45c663ec-33a5-4409-8ace-dc9d77f42434" />

