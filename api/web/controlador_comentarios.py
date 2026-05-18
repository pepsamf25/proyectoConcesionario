from bd import obtener_conexion
import sys
import datetime as dt
from flask import session
from funciones_auxiliares import sanitize_field


def convertir_comentario_a_json(comentario):
    d = {}
    d['id'] = sanitize_field(comentario[0])
    d['usuario'] = sanitize_field(comentario[1])
    d['descripcion'] = sanitize_field(comentario[2])
    return d

#funcino para meter nuevos comentarios a la bd
def insertar_comentario(usuario, descripcion):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO comentarios(usuario, descripcion) VALUES (%s, %s)", (usuario, descripcion))
            conexion.commit()
        conexion.close()
        ret={"status": "OK" }
        code=200
    except:
        ret={"status": "ERROR" }
        print("Excepcion al insertar un comentario", flush=True)
        code=500   
    return ret,code

#fncion para obtener los comentarios de la bd
def obtener_comentarios():
    comentariosjson=[]
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, usuario, descripcion FROM comentarios")
            comentarios = cursor.fetchall()
            if comentarios:
                for comentario in comentarios:
                    comentariosjson.append(convertir_comentario_a_json(comentario))
        conexion.close()
        code=200
    except Exception as e:
        import traceback
        print("Excepcion al consultar todos los comentarios", e, flush=True)
        traceback.print_exc()

        code=500

    # return {"status" : "ERROR", "detalle": str(e)}, 500 
    return comentariosjson,code