from flask import Flask, jsonify, request, g
import os
from flask_wtf.csrf import CSRFProtect 
from variables import cargarvariables
from funciones_auxiliares import sanitize_field
from funciones_auxiliares import prepare_response_extra_headers

def create_app():
    app = Flask(__name__)

    #Configuracion cabecera
    extra_headers=prepare_response_extra_headers(True)

    # configuración...
    app.config.setdefault('DEBUG', True)
    app.config.from_pyfile('settings.py')
    csrf = CSRFProtect(app)

   @app.before_request
    def csrf_protect():
       if not request.path.startswith("/login") and not request.path.startswith("/registro"):
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
