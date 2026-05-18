## TODO:

### Jenkins:

- Solucionar envío de informes.

### Seguridad:
- Inyección XSS:
    - Controlar el Content-type de cada petición  
    - HAY QUE VALIDAR (comparar tipos, tamaño, posibles valores,,) TODOS LOS DATOS QUE SE RECIBEN Y SOBRE TODO SI SON ARCHIVOS
- Cifrado de claves:
    - PEPPER_KEY -> pasar variable de entorno a docker-compose + kubernetes
- Evitar CSRF:
    - Añadir protección a app.py
    - Añadir protección a index.html
    - Añadir token CSRF a las páginas que lo requieran
    - WTF_SECRET_KEY -> pasar variable de entorno a docker-compose + kubernetes
- Establecer cabeceras seguras:
    - Cambiar app.py
    - Cambiar cómo se da la respuesta en todas las rutas
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

