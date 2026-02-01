from __future__ import print_function
import os
import sys
import subprocess
import traceback
from flask import jsonify

#funcion para guardar el fichero 
def guardar_fichero(nombre,contenido):
    try:
        print(nombre, flush=True)
        basepath = os.path.dirname(__file__) # ruta del archivo actual
        print(basepath, flush=True)
        ruta_fichero = os.path.join (basepath,'static/archivos',nombre) 
        print('Archivo guardado en ' +  ruta_fichero, flush=True)
        contenido.save(ruta_fichero)
        respuesta={"status": "OK"}
        code=200
    except:
        print("Excepcion al guardar el fichero", flush=True)  
        respuesta={"status": "ERROR"}
        code=500
    return respuesta, code

#funcion para ver el fichero 
def ver_fichero(nombre):
    try:
        basepath = os.path.dirname(__file__) # ruta del archivo actual
        ruta_fichero = os.path.join (basepath,'static/archivos',nombre) 
        #salida=subprocess.getoutput("cat " + ruta_fichero)
        salida = open(ruta_fichero, "r", encoding="utf-8", errors="replace")
        salida = salida.read()
        respuesta={"contenido": salida}
        code=200
        return respuesta, 200
        
        #ruta_fichero = os.path.join("/app", "static", "archivos", nombre)
        #salida = open(ruta_fichero, "r", encoding="utf-8", errors="replace")
        #respuesta = salida.read()
        #respuesta = {"contenido": respuesta}
        #print(respuesta)
        #return respuesta, 200
    
    except Exception as e:
        print("Excepcion al ver el fichero", e)   
        traceback.print_exc()
        return {"Error": str(e)}, 500    


