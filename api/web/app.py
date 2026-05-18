from flask import Flask, jsonify, request, g
import os
from variables import cargarvariables
from funciones_auxiliares import sanitize_field

def create_app():
    app = Flask(__name__)

    # configuración...
    app.config.setdefault('DEBUG', True)

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
