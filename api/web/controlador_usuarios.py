import logging
import datetime as dt
from flask import current_app, has_app_context
from bd import obtener_conexion
from funciones_auxiliares import cipher_password, compare_password, generate_csrf, create_session, delete_session


def _logger():
    if has_app_context():
        return current_app.logger
    return logging.getLogger(__name__)

#verifica que los datos coinciden con los de la bd
def login_usuario(username,passwordIn):
    conexion = None
    try:
        conexion = obtener_conexion()
        #print(cipher_password(passwordIn))
        with conexion.cursor() as cursor:
            cursor.execute("SELECT perfil,clave,numeroAccesosErroneo,estado FROM usuarios WHERE usuario = %s", (username,))
            usuario = cursor.fetchone()
            
            if usuario is None:
                ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
            else:
                perfil=usuario[0]
                password=usuario[1]
                numAccesosErroneos=usuario[2]
                estado=usuario[3]
                hoy=dt.date.today().strftime('%Y-%m-%d')

                if estado != 'activo':
                    ret = {"status": "ERROR","mensaje":"Usuario bloqueado"}
                elif (compare_password(password, passwordIn)):
                    ret = {"status": "OK",
                           "csrf_token": generate_csrf(),
                           "perfil":perfil}
                    _logger().info("Acceso usuario %s correcto",username)
                    create_session(username,perfil)
                    numAccesosErroneos = 0
                    cursor.execute(
                        "UPDATE usuarios SET numeroAccesosErroneo=%s, fechaUltimoAcceso=%s, estado=%s WHERE usuario = %s",
                        (numAccesosErroneos, hoy, 'activo', username),
                    )
                    conexion.commit()
                else:
                    _logger().info("Acceso usuario %s incorrecto",username)
                    numAccesosErroneos = numAccesosErroneos + 1
                    if numAccesosErroneos > 2:
                        estado = 'bloqueado'
                        _logger().info("Usuario %s bloqueado", username)
                    else:
                        estado = 'activo'
                    cursor.execute(
                        "UPDATE usuarios SET numeroAccesosErroneo=%s, fechaUltimoAcceso=%s, estado=%s WHERE usuario = %s",
                        (numAccesosErroneos, hoy, estado, username),
                    )
                    conexion.commit()
                    ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo"}
            code=200
    except:
        print("Excepcion al validar al usuario")   
        ret={"status":"ERROR"}
        _logger().info("Excepcion al validar al usuario %s", username)
        code=500
    finally:
        try:
            if conexion is not None:
                conexion.close()
        except Exception:
            pass
    return ret,code

#meter el nuevo usuario en la bd
def alta_usuario(username,password,perfil):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s",(username,))
            usuario = cursor.fetchone()
            if usuario is None:
                passwordC=cipher_password(password)
                cursor.execute("INSERT INTO usuarios(usuario,clave,perfil) VALUES(%s,%s,%s)",(username,passwordC,perfil))
                if cursor.rowcount == 1:
                    conexion.commit()
                    _logger().info("Nuevo usuario creado")
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
        print("Excepcion al registrar al usuario")   
        ret={"status":"ERROR"}
        code=500
        _logger().info("Excepcion al registrar al usuario %s", username)
    finally:
        try:
            if conexion is not None:
                conexion.close()
        except Exception:
            pass
    return ret,code     

def logout():
    try:
        delete_session()
        ret={"status":"OK"}
        code=200
        _logger().info("Usuario desconectado")
    except:
        ret={"status":"ERROR"}
        code=500
        _logger().info("Excepcion al desconectar al usuario")
    return ret,code

