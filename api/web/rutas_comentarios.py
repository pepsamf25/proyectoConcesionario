from __future__ import print_function
from flask import request,Blueprint, jsonify, g
from funciones_auxiliares import Encoder
import controlador_comentarios

bp = Blueprint('comentarios', __name__)

@bp.route("/",methods=['POST'])
def login():
     if (validar_session_normal()):
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        comentario_json = g.cleaned_json
        usuario = comentario_json['usuario']
        descripcion = comentario_json['descripcion']
        respuesta,code= controlador_comentarios.insertar_comentario(usuario,descripcion)
        response=make_response(jsonify(respuesta),code)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return response

@bp.route("/",methods=['GET'])
def consultaComentarios():
     if (validar_session_normal()):
    respuesta,code= controlador_comentarios.obtener_comentarios()
    response=make_response(jsonify(respuesta),code)
    return response
