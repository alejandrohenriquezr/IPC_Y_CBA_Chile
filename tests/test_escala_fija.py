"""Regresiones de escala horizontal estable del ranking y sus exportaciones."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class TestEscalaFija(unittest.TestCase):
    def test_plantilla_usa_dominio_temporal_global(self):
        html = (ROOT / 'site' / 'plantilla.html').read_text(encoding='utf-8')
        self.assertIn('function getFixedScale()', html)
        self.assertIn('for(let m=0;m<dates.length;m++)', html)
        self.assertIn('lo*1.1', html)
        self.assertIn('hi*1.1', html)
        self.assertIn('const domain=getFixedScale();', html)
        self.assertNotIn('max0+(max1-max0)*u', html)
        self.assertIn('const zeroX=left+(right-left)*(-domain.min)/span;', html)

    def test_html_generado_coincide_con_plantilla(self):
        html = (ROOT / 'site' / 'index.html').read_text(encoding='utf-8')
        self.assertIn('function getFixedScale()', html)
        self.assertIn("'Escala fija: '", html)

if __name__ == '__main__':
    unittest.main()
