from __future__ import print_function
import logging
import os
import sys
import subprocess
import traceback
from flask import current_app, has_app_context
from flask import jsonify
from werkzeug.utils import secure_filename

# extensiones permitidas por defecto
DEFAULT_ALLOWED = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def _logger():
    if has_app_context():
        return current_app.logger
    return logging.getLogger(__name__)

#funcion para guardar el fichero 
def guardar_fichero(nombre,contenido):
    try:
        if nombre is None or nombre.strip() == "":
            return {"status": "Bad request", "mensaje": "Nombre de archivo no informado"}, 400

        # normalizar nombre y prevenir traversal
        safe_name = secure_filename(nombre)
        if safe_name == "":
            return {"status": "Bad request", "mensaje": "Nombre de archivo inválido"}, 400

        # comprobar extensión
        allowed = DEFAULT_ALLOWED
        try:
            cfg_allowed = current_app.config.get('ALLOWED_FILE_EXTENSIONS')
            if cfg_allowed:
                allowed = set(cfg_allowed)
        except Exception:
            pass
        ext = os.path.splitext(safe_name)[1].lower().lstrip('.')
        if ext not in allowed:
            return {"status": "Bad request", "mensaje": f"Extensión no permitida: .{ext}"}, 400

        basepath = os.path.dirname(__file__) # ruta del archivo actual
        ruta_dir = os.path.join(basepath,'static', 'archivos')
        os.makedirs(ruta_dir, exist_ok=True)
        ruta_fichero = os.path.join(ruta_dir, safe_name)

        # Guardar fichero de forma segura
        contenido.save(ruta_fichero)
        respuesta={"status": "OK", "filename": safe_name}
        code=200
        _logger().info("Fichero %s guardado correctamente", safe_name)
    except Exception:
        print("Excepcion al guardar el fichero", flush=True)
        respuesta={"status": "ERROR"}
        code=500
        _logger().info("Excepcion al guardar el fichero %s", nombre)
    return respuesta, code

#funcion para ver el fichero 
def ver_fichero(nombre):
    try:
        # prevenir traversal y usar secure_filename
        safe_name = secure_filename(nombre)
        if safe_name == "":
            return {"status": "Bad request", "mensaje": "Nombre de archivo inválido"}, 400

        basepath = os.path.dirname(__file__)
        ruta_dir = os.path.join(basepath, 'static', 'archivos')
        ruta_fichero = os.path.join(ruta_dir, safe_name)
        if not os.path.exists(ruta_fichero):
            return {"status": "Not found"}, 404

        with open(ruta_fichero, "r", encoding="utf-8", errors="replace") as salida:
            contenido = salida.read()

        respuesta = {"contenido": contenido}
        _logger().info("Fichero %s leído correctamente", safe_name)
        return respuesta, 200

    except Exception as e:
        print("Excepcion al ver el fichero", e)
        _logger().info("Excepcion al ver el fichero %s: %s", nombre, e)
        traceback.print_exc()
        return {"Error": str(e)}, 500


