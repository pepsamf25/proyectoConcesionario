from bd import obtener_conexion
from calculos import calculariva


def convertir_coche_a_json(coche):
    d = {}
    d['id'] = coche[0]
    d['nombre'] = coche[1]
    d['descripcion'] = coche[2]
    d['precio'] = float(coche[3])
    d['precioiva'] = float(calculariva(float(coche[3])))
    d['foto'] = coche[4]
    return d         

#funcion para meter el coche en la bd
def insertar_coche(nombre, descripcion, precio, foto):
    
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO coches(nombre, descripcion, precio, foto) VALUES (%s, %s, %s,%s)",
                       (nombre, descripcion, precio,foto))
    conexion.commit()
    conexion.close()
    ret={"status": "OK" }
    code=200
    return ret,code

#funcion para tomar los coches de la bd
def obtener_coches():
    cochesjson=[]
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio, foto FROM coches")
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

#tomar un solo coche de la bd
def obtener_coche_por_id(id):
    cochejson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio, foto FROM coches WHERE id =" + id)
            coche = cursor.fetchone()
            if coche is not None:
                cochejson = convertir_coche_a_json(coche)
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar un coche", flush=True)
        code=500
    return cochejson,code

#funcion para eliminar un coche determinado mediante el id
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

#funcion para modificar la info del coche mediante el id
def actualizar_coche(id, nombre, descripcion, precio, foto):
    try:
        conexion = obtener_conexion()
        
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE coches SET nombre=%s, descripcion=%s, precio=%s, foto=%s WHERE id=%s",
                (nombre, descripcion, precio, foto, id)
            )
            conexion.commit()

            if cursor.rowcount == 1:
                return {"status": "OK"}, 200
            else:
                return {"status": "Failure", "detalle": "No se actualizó ninguna fila"}, 404

    except Exception as e:
        import traceback
        print(f"Excepcion al actualizar un coche: {e}", flush=True)
        traceback.print_exc()
        return {"status": "ERROR", "detalle": str(e)}, 500

    finally:
        try:
            conexion.close()
        except:
            pass


