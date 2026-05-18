## TODO:

### Jenkins:

- Solucionar envío de informes.

### Seguridad:
- Inyección XSS:
    - Controlar el Content-type de cada petición 
    - Utilizar el método before_request en el archivo app.py
    - En todas las rutas se utiliza g.cleaned_json. 
    - HAY QUE VALIDAR (comparar tipos, tamaño, posibles valores,,) TODOS LOS DATOS QUE SE RECIBEN Y SOBRE TODO SI SON ARCHIVOS
    - Sanitizar/Codificar la salida: en todos los controladores donde se devuelvan datos. Por ejemplo, en el archivo controladores_chuches.py
- Cifrado de claves:
    - Utilizar funciones en controlador_usuarios.py: login_usuario y alta_usuario
- Evitar CSRF:
    - Añadir protección a app.py
    - Añadir protección a index.html
    - Añadir token CSRF a las páginas que lo requieran
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

