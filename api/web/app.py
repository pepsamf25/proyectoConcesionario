from flask import Flask, jsonify, request, g
import os
from flask_wtf.csrf import CSRFProtect 
from variables import cargarvariables
from funciones_auxiliares import sanitize_field
from funciones_auxiliares import prepare_response_extra_headers
from logging.config import dictConfig

os.makedirs("logs", exist_ok=True)


csrf = CSRFProtect()


dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "logs/flask.log",
                "formatter": "default",
            },
            "time-rotate": {
               "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": "logs/flask.log",
                "when": "D",
                "interval": 10,
                "backupCount": 5,
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console","time-rotate"]},
    }

)

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')
    # Seguridad: limitar el tamaño máximo de subida (por defecto 5MB)
    app.config.setdefault('MAX_CONTENT_LENGTH', int(os.environ.get('MAX_CONTENT_LENGTH', 5 * 1024 * 1024)))
    # Tipos de fichero permitidos (extensiones sin punto)
    app.config.setdefault('ALLOWED_FILE_EXTENSIONS', set(os.environ.get('ALLOWED_FILE_EXTENSIONS', 'txt,png,jpg,jpeg,gif,pdf').split(',')))
    app.config.setdefault('WTF_CSRF_CHECK_DEFAULT', False)
    csrf.init_app(app)

    #Configuracion cabecera
    extra_headers=prepare_response_extra_headers(True)

    # configuración...
    app.config.setdefault('DEBUG', True)
    app.config.from_pyfile('settings.py', silent=True)

    @app.before_request
    def csrf_protect():
         if request.path not in ("/api/usuarios/login", "/api/usuarios/registro"):
           csrf.protect()

    @app.before_request
    def clean_request():
        if request.is_json:
            data = request.get_json(silent=True)
            if data is not None:
                g.cleaned_json = sanitize_field(data)
            else:
                g.cleaned_json = {}
        else:
            g.cleaned_json = {}

    @app.after_request
    def afterRequest(response):
        response.headers['Server'] = 'API'
        app.logger.info(
            "path: %s | method: %s | status: %s | size: %s >>> %s",
            request.path,
            request.method,
            response.status,
            response.content_length,
            request.remote_addr,
        )
        response.headers.extend(extra_headers)
        return response
    #Configuracion sesiones con cookies
    app.config.update(PERMANENT_SESSION_LIFETIME=600)
    #app.config.update( SESSION_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax',) #CON HTTPS
    app.config.update( SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax',)  # CON HTTP

    # Importar y registrar blueprints aquí (evita side-effects en import)
    from rutas_usuarios import bp as usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')

    #api.web
    from rutas_coches import bp as coches_bp
    app.register_blueprint(coches_bp, url_prefix='/api/coches')

    from rutas_ficheros import bp as ficheros_bp
    app.register_blueprint(ficheros_bp, url_prefix='/api/ficheros')

    from rutas_comentarios import bp as comentarios_bp
    app.register_blueprint(comentarios_bp, url_prefix='/api/comentarios')

    @app.errorhandler(500)
    def server_error(error):
        print('An exception occurred during a request. ERROR: ', error, flush=True)
        ret={"status": "Internal Server Error"}
        return jsonify(ret), 500

    return app

if __name__ == '__main__':
    app=create_app()
    #cargarvariables() # ocultar en caso de lanzar todos los contenedores
    try:
        port = int(os.environ.get('PORT'))
        host = os.environ.get('HOST')
        app.run(host=host, port=port)
    except:
        print("Error starting server", flush=True)
