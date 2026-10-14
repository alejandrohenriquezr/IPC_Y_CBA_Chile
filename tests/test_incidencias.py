"""Pruebas de consistencia de incidencias IPC y contribuciones experimentales."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from _excel import sheets

class TestIncidencias(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.book=sheets(ROOT/'data/ipc_cba_actualizado.xlsx')
    def test_registros_incidentes_por_periodo(self):
        ipc=self.book['IPC series'];inc=self.book['IPC incidencias']
        self.assertEqual(len(inc)-1,(len(ipc)-1)*(len(ipc[0])-5))
    def test_no_reetiquetar_contribucion_cba_como_oficial(self):
        rows=self.book['CBA incidencias estimadas']
        self.assertTrue(rows[1:])
        self.assertTrue(all('no CBA oficial' in str(row[8]) for row in rows[1:]))
    def test_contribuciones_cierran_una_variacion_de_subtotal(self):
        rows=self.book['CBA incidencias estimadas']; by_code={};months=set()
        for row in rows[1:]:
            by_code.setdefault(str(row[0]),{})[str(row[2])]=(float(row[3]),float(row[5]),float(row[6]))
            months.add(str(row[2]))
        last=max(months);base=min(months)
        numerator=sum(v[last][0]*(v[last][1]-1) for v in by_code.values())
        denominator=sum(v[base][0]*v[base][1] for v in by_code.values())
        total=100*numerator/denominator
        combined=sum(v[last][2] for v in by_code.values())
        self.assertAlmostEqual(total,combined,places=5)
    def test_incidente_real_con_ponderacion_y_signo(self):
        rows=[r for r in self.book['IPC incidencias'][1:] if str(r[3])=='1.1.1.1.1' and str(r[4])=='2026-09']
        self.assertEqual(len(rows),1)
        self.assertGreater(float(rows[0][5]),0)
        self.assertIsInstance(float(rows[0][6]),float)
if __name__=='__main__':unittest.main()
