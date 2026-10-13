"""Valida la consistencia de códigos padre-hijo para la navegación IPC."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from _excel import sheets


class TestJerarquiaIPC(unittest.TestCase):
    def test_categorias_con_padres_existentes(self):
        # La ruta jerárquica depende del código, no de la glosa.
        filas = sheets(ROOT / 'data/ipc_cba_actualizado.xlsx')['IPC series'][1:]
        categorias = {(int(r[0]), str(r[3])) for r in filas if len(r) > 3 and r[0] is not None and r[3] is not None}
        self.assertTrue(categorias)
        for nivel, codigo in categorias:
            if nivel == 1:
                continue
            padre = codigo.rsplit('.', 1)[0]
            with self.subTest(codigo=codigo):
                self.assertIn((nivel - 1, padre), categorias)

    def test_hijos_directos(self):
        # Los niveles deben contener exactamente un segmento adicional de código.
        filas = sheets(ROOT / 'data/ipc_cba_actualizado.xlsx')['IPC series'][1:]
        for r in filas:
            if not r or r[0] is None or r[3] is None:
                continue
            self.assertEqual(str(r[3]).count('.') + 1, int(r[0]))


if __name__ == '__main__':
    unittest.main()
