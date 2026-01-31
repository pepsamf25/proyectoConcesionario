import unittest
from calculos import calculariva


class TestCalcularIVA(unittest.TestCase):

    def testivade100(self):
        resultado = calculariva(100)
        self.assertEqual(resultado, 21)

if __name__ == "__main__":
        unittest.main()