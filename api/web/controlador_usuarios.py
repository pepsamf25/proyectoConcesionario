from bd import obtener_conexion
import sys
import datetime as dt

#verifica que los datos coinciden con los de la bd
def login_usuario(username,password):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT perfil FROM usuarios WHERE usuario = '" + username +"' and clave= '" + password + "'")
            usuario = cursor.fetchone()
            
            if usuario is None:
                ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
            else:
                ret = {"status": "OK" }
        code=200
        conexion.close()
    except:
        print("Excepcion al validar al usuario", flush=True)   
        ret={"status":"ERROR"}
        code=500
    return ret,code

#meter el nuevo usuario en la bd
def alta_usuario(username,password,perfil):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s",(username,))
            usuario = cursor.fetchone()
            if usuario is None:
                cursor.execute("INSERT INTO usuarios(usuario,clave,perfil) VALUES('"+ username +"','"+  password+"','"+ perfil+"')")
                if cursor.rowcount == 1:
                    conexion.commit()
                    ret={"status": "OK" }
                    code=200
                else:
                    ret={"status": "ERROR" }
                    code=500
            else:
                ret = {"status": "ERROR","mensaje":"Usuario ya existe" }
                code=200
        conexion.close()
    except:
        print("Excepcion al registrar al usuario", flush=True)   
        ret={"status":"ERROR"}
        code=500
    return ret,code    

def logout():
    return {"status":"OK"},200

