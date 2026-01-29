from bd import obtener_conexion
import sys


def convertir_coche_a_json(coche):
    d = {}
    d['id'] = coche[0]
    d['nombre'] = coche[1]
    d['descripcion'] = coche[2]
    d['precio'] = float(coche[3])
    d['foto'] = coche[4]
    d['ingredientes']=coche[5]
    return d

def insertar_coche(nombre, descripcion, precio,foto,ingredientes):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO coches(nombre, descripcion, precio,foto) VALUES (%s, %s, %s,%ss)",
                       (nombre, descripcion, precio,foto))
    conexion.commit()
    conexion.close()
    ret={"status": "OK" }
    code=200
    return ret,code

def obtener_coches():
    cochesjson=[]
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio,foto,ingredientes FROM coches")
            coches = cursor.fetchall()
            if coches:
                for coche in coches:
                    cochesjson.append(convertir_coche_a_json(coche))
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar todas las coches", flush=True)
        code=500
    return cochesjson,code

def obtener_coche_por_id(id):
    cochejson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio,foto,ingredientes FROM coches WHERE id =" + id)
            coche = cursor.fetchone()
            if coche is not None:
                cochejson = convertir_coche_a_json(coche)
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar una coche", flush=True)
        code=500
    return cochejson,code
def eliminar_coche(id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM coches WHERE id = %s", (id,))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar una coche", flush=True)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def actualizar_coche(id, nombre, descripcion, precio, foto,ingredientes):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE coches SET nombre = %s, descripcion = %s, precio = %s, foto=%s, ingredientes=%s WHERE id = %s",
                       (nombre, descripcion, precio, foto,ingredientes,id))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al actualziar una coche", flush=True)
        ret = {"status": "Failure" }
        code=500
    return ret,code
