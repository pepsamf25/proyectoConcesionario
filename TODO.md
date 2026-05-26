## TODO:

### Jenkins:

- Solucionar envío de informes.

### Seguridad:
- Inyección XSS:
    - HAY QUE VALIDAR (comparar tipos, tamaño, posibles valores...) TODOS LOS DATOS QUE SE RECIBEN Y SOBRE TODO SI SON ARCHIVOS
- Cifrado de claves:
    - PEPPER_KEY -> pasar variable de entorno a docker-compose + kubernetes
- Evitar CSRF:
    - WTF_SECRET_KEY -> pasar variable de entorno a docker-compose + kubernetes
- Gestionar la sesión segura:
    - Con auth
    - Con tokens
- Comprobar que subir archivos y ver archivos este securizado
- Conexión a la base de datos segura
- Configurar python para utilizar https
- Configurar docler-compose.yml para despliegue