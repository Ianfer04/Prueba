import unittest
from librodiario import LibroDiario, MontoInvalidoError

class TestLibroDiario(unittest.TestCase):

    def setUp(self):
        self.libro = LibroDiario()

    def test_instancia_correcta(self):
        self.assertIsInstance(self.libro, LibroDiario)
        self.assertEqual(self.libro.transacciones, [])

    def test_agregar_transaccion_valida(self):
        self.libro.agregar_transaccion("01/07/2025", "Venta", 100.0, "ingreso")
        self.assertEqual(len(self.libro.transacciones), 1)
        self.assertEqual(self.libro.transacciones[0]['monto'], 100.0)

    def test_excepcion_monto_negativo(self):
        with self.assertRaises(ValueError):
            self.libro.agregar_transaccion("01/07/2025", "Compra", -50.0, "egreso")

    def test_excepcion_tipo_invalido(self):
        with self.assertRaises(ValueError):
            self.libro.agregar_transaccion("01/07/2025", "Compra", 50.0, "otro")

    def test_calcular_resumen(self):
        self.libro.agregar_transaccion("01/07/2025", "Venta", 200.0, "ingreso")
        self.libro.agregar_transaccion("02/07/2025", "Compra", 100.0, "egreso")
        resumen = self.libro.calcular_resumen()
        self.assertIn("ingresos", resumen)
        self.assertIn("egresos", resumen)
        self.assertIsInstance(resumen["ingresos"], float)
        self.assertIsInstance(resumen["egresos"], float)
        self.assertEqual(resumen["ingresos"], 200.0)
        self.assertEqual(resumen["egresos"], 100.0)

if __name__ == '__main__':
    unittest.main()
