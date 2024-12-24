# auth_service 🛡️

¡Bienvenido a **auth_service**! 🚀

Este microservicio de autenticación está diseñado para gestionar y verificar las credenciales de usuario en aplicaciones distribuidas. Proporciona una interfaz RESTful para operaciones de inicio de sesión, registro y gestión de contraseñas. 🔐

## Características principales ✨

- **Registro de usuarios**: Permite a los usuarios crear nuevas cuentas proporcionando información básica. 📝
- **Inicio de sesión**: Autentica a los usuarios existentes mediante credenciales válidas. 🔑
- **Restablecimiento de contraseñas**: Facilita la recuperación de contraseñas olvidadas a través de un proceso seguro. 🔄
- **Gestión de sesiones**: Administra sesiones de usuario activas y proporciona tokens de acceso para operaciones autenticadas. 🖥️

## Tecnologías utilizadas 🛠️

- **Lenguaje**: Python 3.10 🐍
- **Framework**: Django Rest Framework 🏗️
- **Base de datos**: PostgreSQL 🗃️
- **Autenticación**: JWT (JSON Web Tokens) 🔏

## Instalación 🛠️

1. Clona el repositorio:

   ```bash
   git clone https://github.com/ferxho28/auth_service.git
   cd auth_service
   ```
2.Crea un entorno virtual e instala las dependencias:
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```
3.Configura las variables de entorno necesarias:
```bash
export DJANGO_SECRET_KEY='tu_clave_secreta'
export DATABASE_URL='postgres://usuario:contraseña@localhost:5432/auth_service_db'
```
- **Asegúrate de reemplazar 'tu_clave_secreta' y 'postgres://usuario:contraseña@localhost:5432/auth_service_db' con tus valores reales. 🔑

4.Realiza las migraciones de la base de datos:
```bash

python manage.py migrate
```
Inicia el servidor de desarrollo:
```bash

python manage.py runserver
```
## El servicio estará disponible en http://127.0.0.1:8000/. 🌐


# Guía de Uso de la API de Autenticación

## 1. Registro de Usuario 📝

- **Ruta**: `POST /register/`
- **Descripción**: Permite a un nuevo usuario registrarse proporcionando un nombre de usuario, correo electrónico y contraseña.
- **Datos de entrada**:

  ```json
  {
    "username": "nuevo_usuario",
    "email": "usuario@ejemplo.com",
    "password": "contraseña_segura"
  }
  ```
## Respuesta esperada:
  ```json

    {
      "message": "Usuario registrado exitosamente"
    }
  ```

 ## 2. Inicio de Sesión 🔑

    Ruta: POST /login/

    Descripción: Autentica a un usuario existente y devuelve un par de tokens JWT: uno de acceso y otro de actualización.

    Datos de entrada:
    ```json
    {
      "username": "usuario_existente",
      "password": "contraseña_segura"
    }
    ```
## Respuesta esperada:

    {
      "access_token": "token_de_acceso_jwt",
      "refresh_token": "token_de_actualizacion_jwt"
    }

## 3. Refrescar Token de Acceso 🔄

    Ruta: POST /token/refresh/

    Descripción: Permite obtener un nuevo token de acceso utilizando el token de actualización.

    Datos de entrada:
```json

{
  "refresh": "token_de_actualizacion_jwt"
}
```
## Respuesta esperada:
```json

    {
      "access": "nuevo_token_de_acceso_jwt"
    }
```
## 4. Cerrar Sesión 🚪

    Ruta: POST /logout/

    Descripción: Invalida el token de acceso actual, cerrando la sesión del usuario.

    Datos de entrada:
```json

{
  "access": "token_de_acceso_jwt"
}
```
Respuesta esperada:
```json

    {
      "message": "Sesión cerrada exitosamente"
    }
```
## 5. Obtener Perfil de Usuario 👤

    Ruta: GET /profile/

    Descripción: Recupera la información del perfil del usuario autenticado.

    Encabezados requeridos:

Authorization: Bearer token_de_acceso_jwt

## Respuesta esperada:
```json

    {
      "username": "usuario_existente",
      "email": "usuario@ejemplo.com",
      "date_joined": "2024-12-24T11:56:24Z"
    }
```

## 6. Solicitar Restablecimiento de Contraseña 🔒

    Ruta: POST /password/reset/

    Descripción: Envía un correo electrónico con un enlace para restablecer la contraseña.

    Datos de entrada:
```json


{
  "email": "usuario@ejemplo.com"
}
```
## Respuesta esperada:
```json

    {
      "message": "Correo de restablecimiento de contraseña enviado"
    }
```
## 7. Confirmar Restablecimiento de Contraseña 🔑

    Ruta: POST /password/reset/confirm/

    Descripción: Permite al usuario establecer una nueva contraseña utilizando un token de restablecimiento.

    Datos de entrada:
```json

{
  "token": "token_de_restablecimiento",
  "new_password": "nueva_contraseña_segura",
  "new_password2": "nueva_contraseña_segura"
}
```
## Respuesta esperada:
```json

    {
      "message": "Contraseña actualizada exitosamente"
    }
```
## Consideraciones Adicionales ⚠️

    Asegúrate de que las solicitudes a rutas protegidas incluyan el encabezado Authorization con el formato Bearer token_de_acceso_jwt.
    Utiliza herramientas como Postman o cURL para realizar las solicitudes HTTP.
    Para obtener más información sobre la autenticación y permisos en Django Rest Framework, puedes consultar la documentación oficial.

