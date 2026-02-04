import unittest
from calculos import calculariva


class TestCalcularIVA(unittest.TestCase):

    def test_iva_de_100(self):
        """Test: IVA del 21% sobre 100 euros"""
        resultado = calculariva(100)
        self.assertEqual(resultado, 21)

    def test_iva_de_0(self):
        """Test: IVA sobre 0 euros"""
        resultado = calculariva(0)
        self.assertEqual(resultado, 0)

    def test_iva_de_numero_decimal(self):
        """Test: IVA con número decimal"""
        resultado = calculariva(50.5)
        self.assertAlmostEqual(resultado, 10.605, places=2)

    def test_iva_de_numero_negativo(self):
        """Test: IVA con número negativo (edge case)"""
        resultado = calculariva(-100)
        self.assertEqual(resultado, -21)

    def test_iva_de_numero_grande(self):
        """Test: IVA con número grande"""
        resultado = calculariva(10000)
        self.assertEqual(resultado, 2100)

    def test_iva_precision(self):
        """Test: Verificar precisión del cálculo"""
        importe = 1234.56
        resultado = calculariva(importe)
        esperado = importe * 0.21
        self.assertAlmostEqual(resultado, esperado, places=10)


if __name__ == "__main__":
    unittest.main()
