from flask import request, Blueprint, jsonify
# api.web.
import controlador_coches as controlador_coches
from funciones_auxiliares import Encoder

bp = Blueprint('coches', __name__)

@bp.route("/",methods=["GET"])
def coches():
    respuesta,code= controlador_coches.obtener_coches()
    return jsonify(respuesta), code
    
@bp.route("/<id>",methods=["GET"])
def coche_por_id(id):
    respuesta,code = controlador_coches.obtener_coche_por_id(id)
    return jsonify(respuesta), code

@bp.route("/",methods=["POST"])
def guardar_coche():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        coche_json = request.json
        nombre = coche_json["nombre"]
        descripcion = coche_json["descripcion"]
        precio=coche_json["precio"]
        foto=coche_json["foto"]
        respuesta,code=controlador_coches.insertar_coche(nombre, descripcion,precio,foto)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code

@bp.route("/<int:id>", methods=["DELETE"])
def eliminar_coche(id):
    respuesta,code=controlador_coches.eliminar_coche(id)
    return jsonify(respuesta), code

@bp.route("/", methods=["PUT"])
def actualizar_coche():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        coche_json = request.json
        id = coche_json["id"]
        nombre = coche_json["nombre"]
        descripcion = coche_json["descripcion"]
        precio=float(coche_json["precio"])
        foto=coche_json["foto"]
        respuesta,code=controlador_coches.actualizar_coche(id,nombre,descripcion,precio,foto)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code

