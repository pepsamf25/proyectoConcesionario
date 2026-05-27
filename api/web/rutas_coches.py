from flask import request, Blueprint, jsonify, g, make_response
# api.web.
import controlador_coches as controlador_coches
from funciones_auxiliares import Encoder, validar_session_normal, prepare_response_extra_headers

bp = Blueprint('coches', __name__)

@bp.route("/", methods=["GET"])
def coches():
    if validar_session_normal():
        respuesta, code = controlador_coches.obtener_coches()
        response = make_response(jsonify(respuesta), code)
        return response
    return make_response(jsonify({"status": "Unauthorized"}), 401)


@bp.route("/<id>", methods=["GET"])
def coche_por_id(id):
    if validar_session_normal():
        respuesta, code = controlador_coches.obtener_coche_por_id(id)
        response = make_response(jsonify(respuesta), code)
        return response
    return make_response(jsonify({"status": "Unauthorized"}), 401)


@bp.route("/", methods=["POST"])
def guardar_coche():
    if validar_session_normal():
        if request.is_json:
            coche_json = g.cleaned_json
            nombre = coche_json["nombre"]
            descripcion = coche_json["descripcion"]
            precio = coche_json["precio"]
            foto = coche_json["foto"]
            respuesta, code = controlador_coches.insertar_coche(nombre, descripcion, precio, foto)
            response = make_response(jsonify(respuesta), code)
            return response
        else:
            return make_response(jsonify({"status": "Bad request"}), 400)
    return make_response(jsonify({"status": "Unauthorized"}), 401)


@bp.route("/<int:id>", methods=["DELETE"])
def eliminar_coche(id):
    if validar_session_normal():
        respuesta, code = controlador_coches.eliminar_coche(id)
        response = make_response(jsonify(respuesta), code)
        return response
    return make_response(jsonify({"status": "Unauthorized"}), 401)


@bp.route("/", methods=["PUT"])
def actualizar_coche():
    if validar_session_normal():
        if request.is_json:
            coche_json = g.cleaned_json
            id = coche_json["id"]
            nombre = coche_json["nombre"]
            descripcion = coche_json["descripcion"]
            precio = float(coche_json["precio"])
            foto = coche_json["foto"]
            respuesta, code = controlador_coches.actualizar_coche(id, nombre, descripcion, precio, foto)
            response = make_response(jsonify(respuesta), code)
            return response
        else:
            return make_response(jsonify({"status": "Bad request"}), 400)
    return make_response(jsonify({"status": "Unauthorized"}), 401)

