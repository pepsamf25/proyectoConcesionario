from __future__ import print_function
from flask import request,Blueprint, jsonify, g
from funciones_auxiliares import Encoder
import controlador_usuarios

bp = Blueprint('usuarios', __name__)

@bp.route("/login",methods=['POST'])
def login():
     if (validar_session_normal()):
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = g.cleaned_json
        username = login_json['username']
        password = login_json['password']
        respuesta,code= controlador_usuarios.login_usuario(username,password)
        response=make_response(jsonify(respuesta),code)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return response

@bp.route("/registro",methods=['POST'])
def registro():
     if (validar_session_normal()):
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = g.cleaned_json
        username = login_json['username']
        password = login_json['password']
        profile = login_json['profile']
        respuesta,code= controlador_usuarios.alta_usuario(username,password,profile)
        response=make_response(jsonify(respuesta),code)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return response

@bp.route("/logout",methods=['GET'])
def logout():
     if (validar_session_normal()):
    respuesta,code= controlador_usuarios.logout()
    response=make_response(jsonify(respuesta),code)
    return response

