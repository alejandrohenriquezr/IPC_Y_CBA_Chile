"""Comprueba opciones y separación entre reproducción y exportación."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestVelocidadInterfaz(unittest.TestCase):
    def test_selector_y_reloj_de_reproduccion(self):
        """La vista contiene las velocidades permitidas y el intervalo base."""
        text = (ROOT / 'site/plantilla.html').read_text(encoding='utf-8')
        self.assertIn('id="playSpeed"', text)
        for speed in ('0.75', '1', '1.25', '1.5'):
            self.assertIn(f'value="{speed}"', text)
        self.assertIn('PLAY_INTERVAL_1X_MS=1600', text)
        self.assertIn('PLAY_INTERVAL_1X_MS/playbackRate', text)

    def test_exportaciones_a_uno_x(self):
        """Los codificadores no dependen del control de velocidad interactivo."""
        text = (ROOT / 'site/plantilla.html').read_text(encoding='utf-8')
        self.assertIn('const fps=15;', text)
        self.assertIn('const steps=24;', text)
        self.assertIn('const steps=8;', text)
        self.assertIn('gifEncode(frames,20)', text)


if __name__ == '__main__':
    unittest.main()
