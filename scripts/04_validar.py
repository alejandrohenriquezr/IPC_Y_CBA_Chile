"""Valida datos, procedencia y controles necesarios antes de publicar."""
from pathlib import Path
import re,json
from _excel import sheets
ROOT=Path(__file__).resolve().parents[1]
def main():
    data=sheets(ROOT/'data/ipc_cba_actualizado.xlsx')
    assert len(data['IPC series'])>=601,'Categorías IPC insuficientes'
    assert data['IPC series'][0][5]=='2024-01'
    rows=data['IPC series'][1:]
    ids=[(int(r[0]),str(r[3])) for r in rows]
    assert all(r[3] not in (None,'') for r in rows),'Faltan códigos jerárquicos IPC'
    assert len(ids)==len(set(ids)),'Códigos IPC duplicados'
    assert sum(int(r[4] or 0) for r in rows if int(r[0])==5)>=55,'Correspondencias CBA perdidas'
    assert all(abs(float(r[5]))<1e-8 for r in rows),'La referencia enero 2024 debe ser cero' 
    cba=data['CBA valores'][1:]
    assert cba and all((r[1] is None)!=(r[2] is None) for r in cba),'CBA: valor duplicado o ausente'
    assert all(float(r[1] if r[1] is not None else r[2])>0 for r in cba)
    # Cada mes oficial tiene fuente ministerial y no puede ser posterior al último IPC.
    ipc_months=set(data['IPC series'][0][5:])
    official_months=[str(r[0]) for r in cba if r[1] is not None]
    assert all(m in ipc_months for m in official_months),'CBA posterior a los datos IPC'
    assert all(str(r[4]).startswith('https://observatorio.ministeriodesarrollosocial.gob.cl/') for r in cba if r[1] is not None),'Falta procedencia oficial CBA'
    html=(ROOT/'site/index.html').read_text(encoding='utf-8')
    for tag in ['const DATA=','const CBA_HIST=','id="cbaMetric"','id="cbaReference"','function renderOfficial()','id="variation"','id="rankHigh"','id="rankLow"','function changeValue(']:
        assert tag in html,f'Falta elemento {tag}'
    js=json.loads(re.search(r'const CBA_HIST=(\{.*?\});',html).group(1))
    assert len(js['months'])==len(cba)
    assert 'Elaboración propia' in html
    estado=json.loads((ROOT/'data/estado_actualizacion.json').read_text(encoding='utf-8'))
    assert estado['ipc_ultimo_mes']==data['IPC series'][0][-1]
    assert estado['cba_oficial_ultimo_mes']==max(official_months)
    print('Validación terminada:',len(cba),'meses de CBA;',len(ids),'códigos IPC')
if __name__=='__main__':main()
