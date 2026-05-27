from __future__ import print_function
from flask import request, Blueprint, jsonify, g, make_response
from funciones_auxiliares import Encoder, validar_session_normal
import controlador_comentarios

bp = Blueprint('comentarios', __name__)

@bp.route("/", methods=['POST'])
def login():
    if validar_session_normal():
        if request.is_json:
            comentario_json = g.cleaned_json
            usuario = comentario_json['usuario']
            descripcion = comentario_json['descripcion']
            respuesta, code = controlador_comentarios.insertar_comentario(usuario, descripcion)
            response = make_response(jsonify(respuesta), code)
            return response
        return make_response(jsonify({"status": "Bad request"}), 400)
    return make_response(jsonify({"status": "Unauthorized"}), 401)


@bp.route("/", methods=['GET'])
def consultaComentarios():
    if validar_session_normal():
        respuesta, code = controlador_comentarios.obtener_comentarios()
        response = make_response(jsonify(respuesta), code)
        return response
    return make_response(jsonify({"status": "Unauthorized"}), 401)
