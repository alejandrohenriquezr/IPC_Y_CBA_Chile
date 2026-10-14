"""Genera el HTML únicamente desde las hojas de datos del Excel principal."""
from pathlib import Path
import json,re,shutil
from datetime import datetime,timezone
from _excel import sheets
ROOT=Path(__file__).resolve().parents[1]

def main():
    book=sheets(ROOT/'data/ipc_cba_actualizado.xlsx')
    rows=book['IPC series'];dates=[str(v) for v in rows[0][5:] if v is not None]
    ipc=[];divs={}
    for r in rows[1:]:
        if len(r)<5 or r[0] is None:continue
        level=int(r[0]);div=str(r[1]);name=str(r[2]);values=r[5:5+len(dates)]
        if len(values)!=len(dates) or any(v is None for v in values):raise ValueError('Serie incompleta '+name)
        row={'l':level,'c':div,'n':name,'v':values}
        if r[3] not in (None,''):row['id']=r[3]
        if r[4] not in (None,0,'0'):row['cba']=True
        ipc.append(row)
        if level==1:divs[div]=name
    data={'dates':dates,'divisions':divs,'rows':ipc}
    cba=[]
    for r in book['CBA valores'][1:]:
        if not r or r[0] is None:continue
        cba.append({'mes':str(r[0]),'oficial':r[1] if len(r)>1 else None,'estimado':r[2] if len(r)>2 else None,'fuente':r[4] if len(r)>4 else ''})
    if not cba:raise ValueError('No hay valores CBA')
    # La serie experimental termina al comenzar los valores oficiales.
    estimated=[x for x in cba if x['estimado'] is not None]
    official=[x for x in cba if x['oficial'] is not None]
    if estimated+official!=cba:raise ValueError('Orden o estado irregular de CBA')
    hist={'months':[x['mes'] for x in cba],'official':[x['oficial'] for x in official],
          'proxy':[x['estimado'] for x in estimated], 'anchor':official[0]['mes'],
          'anchor_value':official[0]['oficial'],'status':'Estimación experimental IPC división 1, no oficial'}
    path=ROOT/'site/index.html';template=(ROOT/'site/plantilla.html').read_text(encoding='utf-8')
    cba_ipc=[[str(r['c']),str(r['n'])] for r in ipc if r['l']==5 and r.get('cba')]
    # Incidencias publicadas: mensual, acumulada anual y doce meses por código.
    raw_inc=book['IPC incidencias']
    ix_dates={month:i for i,month in enumerate(dates)}
    inc_by_id={}
    for row in raw_inc[1:]:
        if len(row)<9 or row[4] not in ix_dates:continue
        ident=str(row[3]); arr=inc_by_id.setdefault(ident,[None]*len(dates))
        arr[ix_dates[row[4]]]=[row[6],row[7],row[8]]
    # Serie calculada para un período no publicado explícitamente como
    # incidencia oficial; se obtiene de la hoja validada del Excel.
    start_by_id={}
    for row in raw_inc[1:]:
        if len(row)<10 or row[4] not in ix_dates:continue
        arr=start_by_id.setdefault(str(row[3]),[None]*len(dates))
        arr[ix_dates[row[4]]]=row[9]
    if len(start_by_id)!=len(ipc):raise ValueError('Falta cobertura de incidencias desde enero 2024')
    expenses={}
    for row in book['CBA incidencias estimadas'][1:]:
        if len(row)>=5 and row[0] is not None:
            expenses[str(row[0])]=row[3]
    if len(expenses)<55:raise ValueError('Correspondencias CBA sin cobertura suficiente')
    cba_total=sum(expenses.values())
    payloads={'IPC_INCIDENCES':inc_by_id,'IPC_START_INCIDENCES':start_by_id,'CBA_EXPENSES':expenses,'CBA_TOTAL':cba_total,
              'CBA_IPC':cba_ipc,'DATA':data,'CBA_HIST':hist,'OFFICIAL_CBA':hist['official'],
              'OFFICIAL_DATES':[x['mes'] for x in official],
              'OFFICIAL_URLS':[x['fuente'] for x in official]}
    # El decodificador JSON identifica el fin exacto de cada literal, incluso si
    # un texto estadístico o metodológico contiene puntos y coma.
    decoder=json.JSONDecoder()
    for name,value in payloads.items():
        prefix='const '+name+'='
        at=template.find(prefix)
        if at<0:raise ValueError('No se encontró variable en plantilla: '+name)
        begin=at+len(prefix)
        if name in ('OFFICIAL_URLS','OFFICIAL_DATES'):
            end=template.index(';',begin)-begin
        else:
            _,end=decoder.raw_decode(template[begin:])
        template=template[:begin]+json.dumps(value,ensure_ascii=False,separators=(',',':'))+template[begin+end:]
    # La plantilla presenta fechas como textos, no necesita fórmulas de generación embebidas.
    path.write_text(template,encoding='utf-8')
    (ROOT/'site/datos').mkdir(parents=True,exist_ok=True)
    shutil.copy2(ROOT/'data/ipc_cba_actualizado.xlsx',ROOT/'site/datos/ipc_cba_actualizado.xlsx')
    (ROOT/'data/cba_series.json').write_text(json.dumps(hist,ensure_ascii=False,indent=2),encoding='utf-8')
    status={
      'generado_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),
      'ipc_ultimo_mes':dates[-1],
      'ipc_primero':dates[0],
      'ipc_categorias':len(ipc),
      'cba_oficial_ultimo_mes':official[-1]['mes'],
      'cba_oficial_meses':len(official),
      'cba_estimado_meses':len(estimated),
      'retroproyeccion':'experimental: IPC división 1; no reproduce deflactor oficial compuesto'
    }
    (ROOT/'data/estado_actualizacion.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'site/datos/estado_actualizacion.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('HTML generado:',len(ipc),'categorías;',len(cba),'meses CBA')
if __name__=='__main__':main()
