"""Pruebas de regresión de fórmulas y propiedades del ranking."""
import unittest

def variacion(actual,anterior):
    if anterior<=0:raise ValueError('Índice no positivo')
    return (actual/anterior-1)*100

class TestIndicadores(unittest.TestCase):
    def test_mensual(self):self.assertAlmostEqual(variacion(102,100),2)
    def test_interanual(self):self.assertAlmostEqual(variacion(110,100),10)
    def test_acumulada(self):self.assertAlmostEqual(variacion(103,100),3)
    def test_cambio_de_base(self):
        # Serie almacenada como variaciones relativas a enero 2024.
        self.assertAlmostEqual(variacion(100+21,100+10),10)
    def test_decrecimiento(self):self.assertAlmostEqual(variacion(90,100),-10)
    def test_ordenamiento(self):
        datos=[('a',-2),('b',3),('c',0)]
        self.assertEqual([x[0] for x in sorted(datos,key=lambda x:x[1])],['a','c','b'])
        self.assertEqual([x[0] for x in sorted(datos,key=lambda x:x[1],reverse=True)],['b','c','a'])
    def test_referencia_inexistente(self):
        serie={'2024-01':100}
        self.assertIsNone(serie.get('2023-12'))
if __name__=='__main__':unittest.main()
