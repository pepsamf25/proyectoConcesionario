import unittest
from unittest.mock import patch, MagicMock, call
from controlador_coches import (
    convertir_coche_a_json,
    insertar_coche,
    obtener_coches,
    obtener_coche_por_id,
    eliminar_coche,
    actualizar_coche
)


class TestConvertirCocheAJson(unittest.TestCase):

    def test_convertir_coche_valido(self):
        """Test: Convertir un coche a JSON correctamente"""
        coche = (1, 'BMW X5', 'SUV deportivo', 50000.00, 'foto.jpg')
        resultado = convertir_coche_a_json(coche)
        
        self.assertEqual(resultado['id'], 1)
        self.assertEqual(resultado['nombre'], 'BMW X5')
        self.assertEqual(resultado['descripcion'], 'SUV deportivo')
        self.assertEqual(resultado['precio'], 50000.0)
        self.assertEqual(resultado['foto'], 'foto.jpg')
        # IVA: 50000 * 0.21 = 10500
        self.assertEqual(resultado['precioiva'], 10500.0)

    def test_convertir_coche_precio_decimal(self):
        """Test: Convertir coche con precio decimal"""
        coche = (2, 'Tesla', 'Eléctrico', 35000.50, 'tesla.jpg')
        resultado = convertir_coche_a_json(coche)
        
        self.assertAlmostEqual(resultado['precio'], 35000.50, places=2)
        self.assertAlmostEqual(resultado['precioiva'], 35000.50 * 0.21, places=2)

    def test_convertir_coche_precio_cero(self):
        """Test: Convertir coche con precio 0"""
        coche = (3, 'Regalo', 'Coche gratis', 0, 'gratis.jpg')
        resultado = convertir_coche_a_json(coche)
        
        self.assertEqual(resultado['precio'], 0.0)
        self.assertEqual(resultado['precioiva'], 0.0)

    def test_convertir_coche_estructura(self):
        """Test: Verificar que tiene todas las claves necesarias"""
        coche = (1, 'Test', 'Test coche', 1000, 'test.jpg')
        resultado = convertir_coche_a_json(coche)
        
        claves_esperadas = ['id', 'nombre', 'descripcion', 'precio', 'precioiva', 'foto']
        for clave in claves_esperadas:
            self.assertIn(clave, resultado)


class TestInsertarCoche(unittest.TestCase):

    @patch('controlador_coches.obtener_conexion')
    def test_insertar_coche_exitoso(self, mock_conexion):
        """Test: Insertar un coche correctamente"""
        mock_cursor = MagicMock()
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.commit.return_value = None
        mock_conexion.return_value.close.return_value = None
        
        resultado, codigo = insertar_coche('Ferrari', 'Deportivo rojo', 200000, 'ferrari.jpg')
        
        self.assertEqual(resultado['status'], 'OK')
        self.assertEqual(codigo, 200)
        mock_conexion.return_value.cursor.return_value.__enter__.return_value.execute.assert_called_once()

    @patch('controlador_coches.obtener_conexion')
    def test_insertar_coche_parametros(self, mock_conexion):
        """Test: Verificar que los parámetros se pasan correctamente"""
        mock_cursor = MagicMock()
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        
        nombre = 'Audi A4'
        descripcion = 'Berlina ejecutiva'
        precio = 40000
        foto = 'audi.jpg'
        
        insertar_coche(nombre, descripcion, precio, foto)
        
        call_args = mock_cursor.execute.call_args
        self.assertIn(nombre, call_args[0][1])
        self.assertIn(descripcion, call_args[0][1])


class TestObtenerCoches(unittest.TestCase):
    """Test cases para obtener_coches"""

    @patch('controlador_coches.obtener_conexion')
    def test_obtener_coches_exitoso(self, mock_conexion):
        """Test: Obtener múltiples coches"""
        mock_cursor = MagicMock()
        coches_bd = [
            (1, 'BMW', 'BWM X5', 50000, 'bmw.jpg'),
            (2, 'Audi', 'Audi A4', 40000, 'audi.jpg')
        ]
        mock_cursor.fetchall.return_value = coches_bd
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.close.return_value = None
        
        resultado, codigo = obtener_coches()
        
        self.assertEqual(codigo, 200)
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0]['nombre'], 'BMW')
        self.assertEqual(resultado[1]['nombre'], 'Audi')

    @patch('controlador_coches.obtener_conexion')
    def test_obtener_coches_vacio(self, mock_conexion):
        """Test: Obtener coches cuando la BD está vacía"""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = None
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.close.return_value = None
        
        resultado, codigo = obtener_coches()
        
        self.assertEqual(codigo, 200)
        self.assertEqual(resultado, [])

    @patch('controlador_coches.obtener_conexion')
    def test_obtener_coches_error(self, mock_conexion):
        """Test: Manejar error al obtener coches"""
        mock_conexion.side_effect = Exception("Error de conexión")
        
        resultado, codigo = obtener_coches()
        
        self.assertEqual(codigo, 500)
        self.assertEqual(resultado, [])


class TestObtenerCochePorId(unittest.TestCase):
    """Test cases para obtener_coche_por_id"""

    @patch('controlador_coches.obtener_conexion')
    def test_obtener_coche_existente(self, mock_conexion):
        """Test: Obtener un coche que existe"""
        mock_cursor = MagicMock()
        coche_encontrado = (1, 'Tesla', 'Tesla Model S', 80000, 'tesla.jpg')
        mock_cursor.fetchone.return_value = coche_encontrado
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.close.return_value = None
        
        resultado, codigo = obtener_coche_por_id('1')
        
        self.assertEqual(codigo, 200)
        self.assertEqual(resultado['id'], 1)
        self.assertEqual(resultado['nombre'], 'Tesla')

    @patch('controlador_coches.obtener_conexion')
    def test_obtener_coche_no_existente(self, mock_conexion):
        """Test: Obtener un coche que no existe"""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.close.return_value = None
        
        resultado, codigo = obtener_coche_por_id('999')
        
        self.assertEqual(codigo, 200)
        self.assertEqual(resultado, {})


class TestEliminarCoche(unittest.TestCase):
    """Test cases para eliminar_coche"""

    @patch('controlador_coches.obtener_conexion')
    def test_eliminar_coche_exitoso(self, mock_conexion):
        """Test: Eliminar un coche correctamente"""
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.commit.return_value = None
        mock_conexion.return_value.close.return_value = None
        
        resultado, codigo = eliminar_coche('1')
        
        self.assertEqual(codigo, 200)
        self.assertEqual(resultado['status'], 'OK')

    @patch('controlador_coches.obtener_conexion')
    def test_eliminar_coche_no_existente(self, mock_conexion):
        """Test: Intentar eliminar un coche que no existe"""
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.commit.return_value = None
        mock_conexion.return_value.close.return_value = None
        
        resultado, codigo = eliminar_coche('999')
        
        self.assertEqual(codigo, 200)
        self.assertEqual(resultado['status'], 'Failure')

    @patch('controlador_coches.obtener_conexion')
    def test_eliminar_coche_error_conexion(self, mock_conexion):
        """Test: Manejar error al eliminar coche"""
        mock_conexion.side_effect = Exception("Error de conexión")
        
        resultado, codigo = eliminar_coche('1')
        
        self.assertEqual(codigo, 500)
        self.assertEqual(resultado['status'], 'Failure')


class TestActualizarCoche(unittest.TestCase):
    """Test cases para actualizar_coche"""

    @patch('controlador_coches.obtener_conexion')
    def test_actualizar_coche_exitoso(self, mock_conexion):
        """Test: Actualizar un coche correctamente"""
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.commit.return_value = None
        mock_conexion.return_value.close.return_value = None
        
        resultado, codigo = actualizar_coche('1', 'Ferrari', 'Deportivo', 250000, 'foto.jpg')
        
        self.assertEqual(codigo, 200)
        self.assertEqual(resultado['status'], 'OK')

    @patch('controlador_coches.obtener_conexion')
    def test_actualizar_coche_no_existente(self, mock_conexion):
        """Test: Actualizar un coche que no existe"""
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.commit.return_value = None
        mock_conexion.return_value.close.return_value = None
        
        resultado, codigo = actualizar_coche('999', 'Test', 'Test', 100, 'test.jpg')
        
        self.assertEqual(codigo, 404)
        self.assertEqual(resultado['status'], 'Failure')


if __name__ == "__main__":
    unittest.main()
