"""Actualiza el libro principal desde índices del XLSX oficial sin modificar datos CBA validados.

La serie oficial monetaria CBA se registra en la hoja «CBA valores» después
 de contrastarla con el PDF mensual. Nunca se inventan montos faltantes.
"""
from pathlib import Path
from collections import defaultdict
import json

from _excel import sheets,replace_sheets
ROOT=Path(__file__).resolve().parents[1]

def main():
    path=ROOT/'data/ipc_cba_actualizado.xlsx'
    canonical=sheets(path);existing=canonical['IPC series']
    source=sheets(ROOT/'data/ipc_fuente.xlsx')['IPC 2023=100']
    hdr=source[3]
    names=['Año','Mes','División','Grupo','Clase','Subclase','Producto','Glosa','Índice']
    col={name:hdr.index(name) for name in names}
    period=set();series=defaultdict(dict);meta={};legacy={}
    levels=['División','Grupo','Clase','Subclase','Producto']
    for r in source[4:]:
        try:year=int(r[col['Año']]);month=int(r[col['Mes']]);index=float(r[col['Índice']])
        except (ValueError,TypeError,IndexError):continue
        date=f'{year:04d}-{month:02d}';period.add(date)
        hierarchy=tuple(str(int(r[col[k]])) for k in levels if r[col[k]] is not None)
        if not hierarchy:continue
        depth=len(hierarchy);div=hierarchy[0];name=str(r[col['Glosa']]).strip()
        code='.'.join(hierarchy);key=(depth,code)
        if date in series[key]:raise ValueError(f'Código IPC duplicado: {code}, {date}')
        series[key][date]=index
        if key in meta and meta[key][0]!=div:raise ValueError('División inconsistente: '+code)
        meta[key]=(div,name)
        legacy[(depth,div,name)]=code
    dates=sorted(period)
    if dates[:1]!=['2024-01'] or len(dates)<33:raise ValueError('Meses IPC inesperados')
    old_by_code={}
    for r in existing[1:]:
        if len(r)<5:continue
        code=str(r[3]) if r[3] not in (None,'') else legacy.get((int(r[0]),str(r[1]),str(r[2])))
        if code:
            if (int(r[0]),code) in old_by_code:raise ValueError('Código IPC repetido en libro '+code)
            old_by_code[(int(r[0]),code)]=r
    updated=[['Nivel','División','Categoría','Código','CBA']+dates]
    for key,values in sorted(series.items()):
        depth,code=key;div,name=meta[key]
        if any(d not in values for d in dates):raise ValueError(f'Índice ausente en {code}')
        base=values[dates[0]]
        if base<=0:raise ValueError(f'Índice inicial inválido: {code}')
        previous=old_by_code.get(key)
        if previous is not None and str(previous[2])!=name:
            print(f'Glosa modificada {code}: {previous[2]} -> {name}')
        updated.append([depth,div,name,code,previous[4] if previous else 0]+
                       [round((values[d]/base-1)*100,6) for d in dates])
    if len(updated)<600:raise ValueError('Disminución inesperada de categorías')
    if sum(1 for row in updated[1:] if row[0]==5 and row[4])<55:
        raise ValueError('Pérdida de correspondencias IPC–CBA')
    # Conservar los importes oficiales y recalcular solo el tramo experimental.
    history=canonical['CBA valores'][1:]
    # Incorporar únicamente los PDF presentes en manifiesto y validados en esta ejecución.
    manifest_path=ROOT/'data/cba_fuentes_validadas.json'
    if manifest_path.exists():
        from _cba_oficial import read_official_pdf
        source_manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
        existing_cba={str(r[0]):list(r) for r in history}
        for item in source_manifest['informes']:
            mes=item['mes'];pdf=ROOT/'data/cba_informes'/(mes+'.pdf')
            value=read_official_pdf(pdf.read_bytes(),mes)
            if value!=item['valor']:raise ValueError('Manifiesto/PDF no concuerdan: '+mes)
            if mes not in dates:raise ValueError('Informe CBA más reciente que IPC; no publicar serie incompleta: '+mes)
            prior=existing_cba.get(mes)
            if prior and prior[1] is not None and int(prior[1])!=value:
                raise ValueError('Revisión oficial modifica monto previamente validado: '+mes)
            existing_cba[mes]=[mes,value,None,'Oficial MDSF',item['fuente']]
        history=[existing_cba[k] for k in sorted(existing_cba)]

    official=next((x for x in history if len(x)>1 and x[1] is not None),None)
    if official is None:raise ValueError('Falta un valor oficial CBA de referencia')
    anchor_month=str(official[0]);anchor_value=float(official[1])
    food=next((v for v in updated[1:] if v[0]==1 and v[1]=='1'),None)
    if food is None:raise ValueError('No existe la división alimentos')
    changes=dict(zip(dates,food[5:]))
    if anchor_month not in changes:raise ValueError('Ancla CBA ausente del IPC')
    cba=[canonical['CBA valores'][0]]
    for row in history:
        x=list(row)+[None]*max(0,5-len(row))
        month=str(x[0])
        if x[1] is None:
            if month not in changes:raise ValueError('Sin IPC para mes CBA '+month)
            x[2]=round(anchor_value*(100+changes[month])/(100+changes[anchor_month]),2)
        else:x[2]=None
        cba.append(x[:5])
    # Actualizar las series vinculadas que son utilizadas por la presentación.
    # Editar el XLSX como OOXML estándar, preservando las otras hojas.
    replace_sheets(path,{'IPC series':updated,'CBA valores':cba})
    print('Excel IPC actualizado:',len(updated)-1,'categorías;',len(dates),'meses')
if __name__=='__main__':main()
