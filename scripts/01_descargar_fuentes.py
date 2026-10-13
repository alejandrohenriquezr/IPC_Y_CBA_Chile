"""Descarga y valida fuentes oficiales; no modifica el Excel principal."""
import argparse
import hashlib
import json
from pathlib import Path
import requests
from _excel import sheets
from _cba_oficial import discover_reports,fetch_validated,CBAValidationError
ROOT=Path(__file__).resolve().parents[1]
IPC_URL='https://www.ine.gob.cl/docs/default-source/%C3%adndice-de-precios-al-consumidor/cuadros-estadisticos/base-anual-2023_100/series-de-tiempo/ipc-xls.xlsx'

def main():
    p=argparse.ArgumentParser();p.add_argument('--actualizar',action='store_true');args=p.parse_args()
    dest=ROOT/'data/ipc_fuente.xlsx';downloads=ROOT/'data/cba_informes'
    if args.actualizar:
        session=requests.Session()
        response=session.get(IPC_URL,timeout=85,headers={'User-Agent':'Mozilla/5.0'});response.raise_for_status()
        temp=dest.with_suffix('.temporal.xlsx');temp.write_bytes(response.content)
        try:
            rows=sheets(temp)['IPC 2023=100']
            if len(rows)<1000:raise ValueError('Serie IPC demasiado corta')
        except Exception:temp.unlink(missing_ok=True);raise
        # Descubrir todos los informes y verificar los PDFs faltantes antes de sustituir fuentes.
        reports=discover_reports(session)
        staged=[]
        for period,url in reports.items():
            local=downloads/(period+'.pdf')
            if local.exists():
                # También revisar fuentes locales para evitar PDFs dañados o incorrectos.
                from _cba_oficial import read_official_pdf
                amount=read_official_pdf(local.read_bytes(),period)
                staged.append((period,url,amount,None))
            else:
                item=fetch_validated(session,period,url)
                staged.append((period,url,item['valor'],item['pdf']))
        downloads.mkdir(parents=True,exist_ok=True)
        for period,url,amount,blob in staged:
            if blob is not None:(downloads/(period+'.pdf')).write_bytes(blob)
        manifest={'informes':[{'mes':month,'valor':value,'fuente':url,'sha256':hashlib.sha256((downloads/(month+'.pdf')).read_bytes()).hexdigest()} for month,url,value,_ in staged]}
        manifest_file=ROOT/'data/cba_fuentes_validadas.json'
        manifest_file.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        temp.replace(dest)
        print('Fuentes descargadas y validadas:',len(staged),'informes CBA')
    if not dest.exists():raise FileNotFoundError('Falta el Excel IPC original')
    print('IPC:',len(sheets(dest)['IPC 2023=100']),'filas; fuente CBA:',('actualizada' if args.actualizar else 'conservada'))
if __name__=='__main__':main()
