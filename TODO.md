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
    - Con auth
    - Con tokens
- Generar logs:
    - Añadir líneas a app.py
    - En cualquier sitio que se quiera grabar en el log escribir app.logger.info("texto").
- Comprobar que subir archivos y ver archivos este securizado
- Conexión a la base de datos segura
- Configurar python para utilizar https

