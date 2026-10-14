"""Comprobaciones de visualización del valor y del inicio temporal válido."""
import unittest
from pathlib import Path

HTML = (Path(__file__).resolve().parents[1] / 'site' / 'plantilla.html').read_text(encoding='utf-8')

class TestEtiquetaEInicio(unittest.TestCase):
    def test_etiquetas_y_unidades(self):
        self.assertIn("valueLabel.textContent=formatRank(v)", HTML)
        self.assertIn("valueLabel.style.left=(v<0?left-w:left+w)+'%'", HTML)
        self.assertIn("ctx.fillText(formatRank(v),tip,y+20)", HTML)
        self.assertIn("minimumFractionDigits:2,maximumFractionDigits:2", HTML)

    def test_mes_inicial_y_exportaciones(self):
        self.assertIn('function firstValidMonth()', HTML)
        self.assertIn("$('range').min=first", HTML)
        self.assertIn("if(index===dates.length-1)index=firstValidMonth()", HTML)
        self.assertEqual(HTML.count('for(let i=firstValidMonth();i<dates.length-1;i++)'),2)

if __name__=='__main__': unittest.main()
