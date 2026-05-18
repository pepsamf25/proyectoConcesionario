## TODO:

### Jenkins:

- Solucionar envío de informes.

### Seguridad:
- Inyección XSS:
    - HAY QUE VALIDAR (comparar tipos, tamaño, posibles valores,,) TODOS LOS DATOS QUE SE RECIBEN Y SOBRE TODO SI SON ARCHIVOS
    - Sanitizar/Codificar la salida: en todos los controladores donde se devuelvan datos. Por ejemplo, en el archivo controladores_chuches.py
- Cifrado de claves:
    - PEPPER_KEY -> pasar variable de entorno a docker-compose + kubernetes
- Evitar CSRF:
    - WTF_SECRET_KEY -> pasar variable de entorno a docker-compose + kubernetes
- Establecer cabeceras seguras:
- Gestionar la sesión segura:
    - Con cookies:
        - Modificar app.py
        - Modificar controlador_usuarios.py
        - En controlador_usuarios.py establecer la ruta de cerrar sesión
        - En todas las rutas comprobar si el usuario tiene permiso o no
    - Con auth
    - Con tokens
- Generar logs:
    - Añadir líneas a app.py
    - En cualquier sitio que se quiera grabar en el log escribir app.logger.info("texto").
- Comprobar que subir archivos y ver archivos este securizado
- Conexión a la base de datos segura
- Configurar python para utilizar https

