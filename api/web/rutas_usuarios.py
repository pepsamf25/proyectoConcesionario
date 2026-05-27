from __future__ import print_function
from flask import request, Blueprint, jsonify, g, make_response
from funciones_auxiliares import Encoder, validar_session_normal
import controlador_usuarios

bp = Blueprint('usuarios', __name__)

@bp.route("/login", methods=['POST'])
def login():
    if request.is_json:
        login_json = g.cleaned_json
        username = login_json['username']
        password = login_json['password']
        respuesta, code = controlador_usuarios.login_usuario(username, password)
        response = make_response(jsonify(respuesta), code)
        return response
    return make_response(jsonify({"status": "Bad request"}), 400)


@bp.route("/registro", methods=['POST'])
def registro():
    if request.is_json:
        login_json = g.cleaned_json
        username = login_json['username']
        password = login_json['password']
        profile = login_json.get('profile', 'normal')
        respuesta, code = controlador_usuarios.alta_usuario(username, password, profile)
        response = make_response(jsonify(respuesta), code)
        return response
    return make_response(jsonify({"status": "Bad request"}), 400)


@bp.route("/logout", methods=['GET'])
def logout():
    if validar_session_normal():
        respuesta, code = controlador_usuarios.logout()
        response = make_response(jsonify(respuesta), code)
        return response
    return make_response(jsonify({"status": "Unauthorized"}), 401)

