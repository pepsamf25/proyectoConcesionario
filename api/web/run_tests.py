import unittest
import sys
from io import StringIO
import time


def ejecutar_pruebas():
    """Ejecuta todas las pruebas y genera un reporte"""
    
    print("=" * 70)
    print("  PRUEBAS UNITARIAS - PROYECTO CONCESIONARIO")
    print("=" * 70)
    print()
    
    loader = unittest.TestLoader()
    
    suite = loader.discover('.', pattern='test_*.py')
    
    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    
    inicio = time.time()
    resultado = runner.run(suite)
    fin = time.time()
    
    # Imprimir resultado
    output = stream.getvalue()
    print(output)
    
    print()
    print("=" * 70)
    print("  RESUMEN DE PRUEBAS")
    print("=" * 70)
    print(f"Tests ejecutados: {resultado.testsRun}")
    print(f"Exitosos: {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f"Fallos: {len(resultado.failures)}")
    print(f"Errores: {len(resultado.errors)}")
    print(f"Tiempo total: {fin - inicio:.3f}s")
    print("=" * 70)
    print()
    
    if resultado.failures:
        for test, traceback in resultado.failures:
            print(f"\n{test}:")
            print(traceback)
    
    if resultado.errors:
        for test, traceback in resultado.errors:
            print(f"\n{test}:")
            print(traceback)
    
    # Retornar código de salida
    if resultado.wasSuccessful():
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(ejecutar_pruebas())
