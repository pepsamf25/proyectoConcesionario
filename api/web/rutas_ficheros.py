from __future__ import print_function
from flask import request, Blueprint, jsonify, make_response
from funciones_auxiliares import validar_session_normal
import controlador_ficheros
import os
import sys
import subprocess

bp = Blueprint('ficheros', __name__)

@bp.route('/', methods=['POST'])
def upload():
    try:
        if validar_session_normal():
            contenido = request.files.get('fichero')
            nombre = request.form.get("nombre")
            if contenido is None:
                return make_response(jsonify({"status": "Bad request", "mensaje": "Falta el fichero"}), 400)
            if nombre is None or nombre.strip() == "":
                return make_response(jsonify({"status": "Bad request", "mensaje": "Falta el nombre"}), 400)
            respuesta, code = controlador_ficheros.guardar_fichero(nombre, contenido)
            response = make_response(jsonify(respuesta), code)
            return response
        return make_response(jsonify({"status": "Unauthorized"}), 401)
    except Exception as e:
        print(f"Error subiendo archivo: {e}", flush=True)
        return make_response(jsonify({"status": "ERROR"}), 500)


@bp.route('/<archivo>', methods=['GET'])
def ver(archivo):
    try:
        if validar_session_normal():
            respuesta, code = controlador_ficheros.ver_fichero(archivo)
            response = make_response(jsonify(respuesta), code)
            return response
        return make_response(jsonify({"status": "Unauthorized"}), 401)
    except:
        return make_response(jsonify({"status": "ERROR"}), 500)

