"""Registra incidencias publicadas por el INE y contribuciones experimentales CBA.

Las incidencias IPC se copian del Excel institucional sin imputaciones. Las
contribuciones CBA utilizan gastos de referencia de los componentes homologados;
no deben interpretarse como incidencias de la serie monetaria oficial de CBA.
"""
from pathlib import Path
from collections import defaultdict
import unicodedata
from _excel import sheets, replace_sheets
ROOT=Path(__file__).resolve().parents[1]

def norm(value):
    return ' '.join(''.join(c for c in unicodedata.normalize('NFD',str(value or '').upper()) if unicodedata.category(c)!='Mn').split())

def run():
    dest=ROOT/'data/ipc_cba_actualizado.xlsx'
    book=sheets(dest)
    source=sheets(ROOT/'data/ipc_fuente.xlsx')['IPC 2023=100']
    header=source[3]
    pos={h:i for i,h in enumerate(header)}
    dates=[str(x) for x in book['IPC series'][0][5:]]
    index={(int(r[0]),str(r[3])):r for r in book['IPC series'][1:]}
    incid=[['Nivel','División','Categoría','Código','Mes','Ponderación IPC (%)','Incidencia mensual (p.p.)','Incidencia acumulada anual (p.p.)','Incidencia 12 meses (p.p.)','Incidencia desde ene. 2024 (p.p.)']]
    for line in source[4:]:
        try: date=f"{int(line[pos['Año']]):04d}-{int(line[pos['Mes']]):02d}"
        except (TypeError,ValueError):continue
        if date not in dates:continue
        codes=[str(int(line[pos[k]])) for k in ['División','Grupo','Clase','Subclase','Producto'] if line[pos[k]] is not None]
        if not codes:continue
        key=(len(codes),'.'.join(codes))
        if key not in index:raise ValueError('Código de incidencia no presente en IPC series: '+str(key))
        orig=index[key]
        incid.append([key[0],orig[1],orig[2],key[1],date,line[pos['Ponderación']],line[pos['Incidencia Mensual (%)']],line[pos['Incidencia Acumulada (%)']],line[pos['Incidencia 12 Meses (%)']]])
    expected=(len(book['IPC series'])-1)*len(dates)
    if len(incid)-1!=expected:raise ValueError(f'Incidencias incompletas: {len(incid)-1}/{expected}')
    # Incidencias desde enero de 2024, calculadas con ponderaciones e índices
    # oficiales y el IPC general del mes inicial como denominador común.
    # Las cifras son calculadas, no corresponden a incidencias publicadas
    # directamente para esta ventana temporal.
    general={}
    category_index=defaultdict(dict)
    category_weight={}
    for line in source[4:]:
        try:
            date=f"{int(line[pos['Año']]):04d}-{int(line[pos['Mes']]):02d}"
            idx=float(line[pos['Índice']])
        except (TypeError, ValueError):
            continue
        if date not in dates:continue
        codes=[str(int(line[pos[k]])) for k in ['División','Grupo','Clase','Subclase','Producto'] if line[pos[k]] is not None]
        if not codes:
            if str(line[pos['Glosa']]).strip().lower()=='ipc general':general[date]=idx
            continue
        key=(len(codes),'.'.join(codes))
        category_index[key][date]=idx
        category_weight[key]=float(line[pos['Ponderación']])
    base_date=dates[0]
    if base_date not in general:raise ValueError('Falta IPC general para enero de 2024')
    if len(general)!=len(dates):raise ValueError('Cobertura incompleta del IPC general')
    start=[['Nivel','División','Categoría','Código','Mes','Ponderación IPC (%)',
            'Índice ene. 2024','Índice mes','IPC general ene. 2024',
            'Incidencia desde ene. 2024 (p.p.)','Variación IPC general desde ene. 2024 (%)']]
    for key,item in sorted(category_index.items()):
        if key not in index or base_date not in item:raise ValueError('Serie IPC sin referencia: '+str(key))
        orig=index[key];w=category_weight[key];base_idx=item[base_date]
        for date in dates:
            if date not in item:raise ValueError('Índice faltante para '+str(key)+' '+date)
            inc=(item[date]-base_idx)*w/general[base_date]
            overall=(general[date]/general[base_date]-1)*100
            start.append([key[0],orig[1],orig[2],key[1],date,w,base_idx,
                          item[date],general[base_date],round(inc,9),round(overall,9)])
    # La suma de incidencias debe reconstruir la variación general en cada mes
    # y nivel de desagregación. 0,01 p.p. admite el redondeo de índices fuente.
    for date in dates:
        target=(general[date]/general[base_date]-1)*100
        for level in range(1,6):
            total=sum(row[9] for row in start[1:] if row[0]==level and row[4]==date)
            if abs(total-target)>0.01:
                raise ValueError(f'Incidencia no aditiva en {date}, nivel {level}: {total} vs {target}')
    # Anexar a la hoja original la ventana histórica calculada y validada.
    start_index={(str(row[3]),str(row[4])):row[9] for row in start[1:]}
    for row in incid[1:]:
        row.append(start_index[(str(row[3]),str(row[4]))])
    # Correspondencias nominales verificables; algunas categorías IPC reúnen más de un componente CBA.
    ipc_names=defaultdict(list)
    for r in book['IPC series'][1:]:
        if int(r[0])==5:ipc_names[(str(r[1]),norm(r[2]))].append(str(r[3]))
    expenses=defaultdict(float)
    unresolved=[]
    for r in book['Correspondencias'][1:]:
        if len(r)<5 or not r[0]:continue
        if r[1] is None or r[4] is None:
            unresolved.append(str(r[0]));continue
        candidates=ipc_names[(str(r[3]),norm(r[1]))]
        if len(candidates)!=1:
            unresolved.append(str(r[0]));continue
        expenses[candidates[0]]+=float(r[4])
    if not expenses:raise ValueError('No hay productos CBA vinculados')
    # La canasta comparable se restringe al subtotal de gastos con correspondencia.
    # Cada gasto se revalúa mediante el índice relativo del producto respecto de enero 2024.
    series={str(r[3]):[float(v) for v in r[5:]] for r in book['IPC series'][1:] if int(r[0])==5}
    coverage=sum(expenses.values())
    cbadata=[['Código producto IPC','Nombre IPC','Mes','Gasto referencia vinculado ($)','Participación en subtotal vinculado (%)','Costo relativo índice ene. 2024','Contribución desde enero 2024 (p.p.)','Cobertura subtotal gasto ($)','Carácter']]
    productnames={str(r[3]):r[2] for r in book['IPC series'][1:] if int(r[0])==5}
    for code,gasto in sorted(expenses.items()):
        weight=gasto/coverage
        for t,month in enumerate(dates):
            factor=1+series[code][t]/100
            cbadata.append([code,productnames[code],month,round(gasto,4),round(weight*100,8),round(factor,10),round(weight*(factor-1)*100,8),round(coverage,4),'Estimación analítica; subtotal vinculado, no CBA oficial'])
    replace_sheets(dest,{'IPC incidencias':incid,'CBA incidencias estimadas':cbadata})
    print('Incidencias IPC:',len(incid)-1,'registros; CBA productos:',len(expenses),'Gasto vinculado:',round(coverage,2),'Sin correspondencia:',len(unresolved))
if __name__=='__main__':run()
