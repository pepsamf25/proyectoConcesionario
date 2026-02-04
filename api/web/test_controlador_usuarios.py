import unittest
from unittest.mock import patch, MagicMock
from controlador_usuarios import login_usuario, alta_usuario, logout


class TestLoginUsuario(unittest.TestCase):

    @patch('controlador_usuarios.obtener_conexion')
    def test_login_usuario_correcto(self, mock_conexion):
        """Test: Login con usuario y contraseña correctos"""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ('admin',)
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.close.return_value = None
        
        resultado, codigo = login_usuario('juan', 'password123')
        
        self.assertEqual(resultado['status'], 'OK')
        self.assertEqual(codigo, 200)

    @patch('controlador_usuarios.obtener_conexion')
    def test_login_usuario_incorrecto(self, mock_conexion):
        """Test: Login con usuario/contraseña incorrectos"""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.close.return_value = None
        
        resultado, codigo = login_usuario('juan', 'wrongpassword')
        
        self.assertEqual(resultado['status'], 'ERROR')
        self.assertIn('Usuario/clave erroneo', resultado['mensaje'])
        self.assertEqual(codigo, 200)

    @patch('controlador_usuarios.obtener_conexion')
    def test_login_usuario_vacio(self, mock_conexion):
        """Test: Login con usuario vacío"""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.close.return_value = None
        
        resultado, codigo = login_usuario('', '')
        
        self.assertEqual(resultado['status'], 'ERROR')
        self.assertEqual(codigo, 200)

    @patch('controlador_usuarios.obtener_conexion')
    def test_login_usuario_error_conexion(self, mock_conexion):
        """Test: Manejar error de conexión en login"""
        mock_conexion.side_effect = Exception("Error de conexión")
        
        resultado, codigo = login_usuario('juan', 'password')
        
        self.assertEqual(resultado['status'], 'ERROR')
        self.assertEqual(codigo, 500)


class TestAltaUsuario(unittest.TestCase):
    """Test cases para alta_usuario"""

    @patch('controlador_usuarios.obtener_conexion')
    def test_alta_usuario_nuevo_exitoso(self, mock_conexion):
        """Test: Registrar un nuevo usuario correctamente"""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_cursor.rowcount = 1
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.commit.return_value = None
        mock_conexion.return_value.close.return_value = None
        
        resultado, codigo = alta_usuario('nuevo_usuario', 'pass123', 'user')
        
        self.assertEqual(resultado['status'], 'OK')
        self.assertEqual(codigo, 200)

    @patch('controlador_usuarios.obtener_conexion')
    def test_alta_usuario_ya_existe(self, mock_conexion):
        """Test: Intentar registrar usuario que ya existe"""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ('admin',)
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.close.return_value = None
        
        resultado, codigo = alta_usuario('juan', 'password', 'user')
        
        self.assertEqual(resultado['status'], 'ERROR')
        self.assertIn('Usuario ya existe', resultado['mensaje'])
        self.assertEqual(codigo, 200)

    @patch('controlador_usuarios.obtener_conexion')
    def test_alta_usuario_fallo_insercion(self, mock_conexion):
        """Test: Cuando falla la inserción en BD"""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_cursor.rowcount = 0
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.commit.return_value = None
        mock_conexion.return_value.close.return_value = None
        
        resultado, codigo = alta_usuario('nuevo', 'pass', 'user')
        
        self.assertEqual(resultado['status'], 'ERROR')
        self.assertEqual(codigo, 500)

    @patch('controlador_usuarios.obtener_conexion')
    def test_alta_usuario_error_conexion(self, mock_conexion):
        """Test: Manejar error de conexión en alta"""
        mock_conexion.side_effect = Exception("Error de conexión")
        
        resultado, codigo = alta_usuario('usuario', 'password', 'admin')
        
        self.assertEqual(resultado['status'], 'ERROR')
        self.assertEqual(codigo, 500)

    @patch('controlador_usuarios.obtener_conexion')
    def test_alta_usuario_con_perfil_admin(self, mock_conexion):
        """Test: Alta de usuario con perfil admin"""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_cursor.rowcount = 1
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.commit.return_value = None
        mock_conexion.return_value.close.return_value = None
        
        resultado, codigo = alta_usuario('admin_nuevo', 'adminpass', 'admin')
        
        self.assertEqual(resultado['status'], 'OK')
        self.assertEqual(codigo, 200)


class TestLogout(unittest.TestCase):
    """Test cases para logout"""

    def test_logout_exitoso(self):
        """Test: Logout siempre retorna OK"""
        resultado, codigo = logout()
        
        self.assertEqual(resultado['status'], 'OK')
        self.assertEqual(codigo, 200)

    def test_logout_tipo_respuesta(self):
        """Test: Logout retorna diccionario y código"""
        resultado, codigo = logout()
        
        self.assertIsInstance(resultado, dict)
        self.assertIsInstance(codigo, int)


class TestIntegracionUsuarios(unittest.TestCase):
    """Casos de integración para usuarios"""

    @patch('controlador_usuarios.obtener_conexion')
    def test_flujo_registro_y_login(self, mock_conexion):
        """Test: Flujo completo de registro y posterior login"""
        mock_cursor = MagicMock()
        mock_conexion.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_conexion.return_value.commit.return_value = None
        mock_conexion.return_value.close.return_value = None
        
        mock_cursor.fetchone.return_value = None
        mock_cursor.rowcount = 1
        
        resultado_registro, codigo_registro = alta_usuario('testuser', 'testpass123', 'user')
        self.assertEqual(resultado_registro['status'], 'OK')
        
        mock_cursor.fetchone.return_value = ('user',)
        resultado_login, codigo_login = login_usuario('testuser', 'testpass123')
        self.assertEqual(resultado_login['status'], 'OK')


if __name__ == "__main__":
    unittest.main()
