"""Descubrimiento, extracción y control del valor oficial mensual de la CBA.

Fuente primaria: informes metodología 2024 del Observatorio Social.
No mezcla informes de la metodología 2013 ni utiliza cifras de cuadros de LP/LPE.
"""
import io
import re
from calendar import month_name
from datetime import date
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pdfplumber
import requests

INDEX_URL = 'https://observatorio.ministeriodesarrollosocial.gob.cl/nueva-serie-cba-2026'
BASE_PDF = 'https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/cba/nueva_serie/{year}/Informe_CBA_{year}_{month:02d}.pdf'
MONTHS = dict(zip(('enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'),range(1,13)))
UA = {'User-Agent':'Mozilla/5.0 (compatible; cba-ipc-research/1.0)'}

class CBAValidationError(ValueError): pass

def normalize(s):
    import unicodedata
    return ''.join(ch for ch in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(ch)!='Mn')

def discover_reports(session=None):
    """Detecta meses publicados en el índice de metodología 2024 (sin adivinar meses)."""
    session=session or requests.Session()
    response=session.get(INDEX_URL,headers=UA,timeout=40);response.raise_for_status()
    soup=BeautifulSoup(response.text,'html.parser')
    discovered={}
    for tr in soup.select('tr'):
        text=normalize(tr.get_text(' ',strip=True))
        if 'canasta basica de alimentos' not in text:continue
        m=re.search(r'\b(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+(20\d{2})\b',text)
        if not m:continue
        month=MONTHS[m.group(1)];year=int(m.group(2))
        if year<2026:continue
        links=[urljoin(INDEX_URL,a.get('href','')) for a in tr.select('a[href]') if '.pdf' in a.get('href','').lower()]
        url=next((v for v in links if 'Informe_CBA_' in v),None) or BASE_PDF.format(year=year,month=month)
        discovered[f'{year:04d}-{month:02d}']=url
    if not discovered:
        raise CBAValidationError('El catálogo no permitió identificar informes mensuales CBA metodología 2024')
    return dict(sorted(discovered.items()))

def read_official_pdf(blob,period):
    """Exige período y monto inequívoco en Cuadro 1, contrastado con texto narrativo."""
    year,mm=map(int,period.split('-'))
    if not blob.startswith(b'%PDF-'):raise CBAValidationError(f'{period}: respuesta no es PDF')
    with pdfplumber.open(io.BytesIO(blob)) as pdf:
        if len(pdf.pages)<5:raise CBAValidationError(f'{period}: informe incompleto')
        text='\n'.join((p.extract_text(layout=False) or '') for p in pdf.pages[:6])
        page=(pdf.pages[4].extract_text(layout=False) or '')
    clean=normalize(text)
    month=next(k for k,v in MONTHS.items() if v==mm)
    if f'{month} de {year}' not in clean:raise CBAValidationError(f'{period}: mes/año no concuerda con documento')
    if 'metodologia 2024' not in clean:raise CBAValidationError(f'{period}: no acredita metodología 2024')
    # La quinta página física contiene el Cuadro 1; solo aceptar su fila CBA.
    if 'Cuadro 1' not in page and 'Cuadro 1' not in text:raise CBAValidationError(f'{period}: no aparece Cuadro 1')
    sec=re.search(r'Cuadro\s*1\s*:',page,re.I)
    if not sec:raise CBAValidationError(f'{period}: no se encontró Cuadro 1 en página 5')
    fragment=page[sec.end():].split('Cuadro 2')[0]
    values=re.findall(r'^\s*CBA\s+\$?\s*(\d{1,3}(?:\.\d{3})+)\s*$',fragment,re.M|re.I)
    if len(values)!=1:raise CBAValidationError(f'{period}: valor CBA ambiguo en Cuadro 1: {values}')
    amount=int(values[0].replace('.',''))
    if not 30000<=amount<=300000:raise CBAValidationError(f'{period}: magnitud fuera de límites plausibles')
    narrative=re.search(r'canasta basica de alimentos.{0,180}?\$\s*(\d{1,3}(?:\.\d{3})+)',normalize(text),re.S)
    if narrative and int(narrative.group(1).replace('.',''))!=amount:
        raise CBAValidationError(f'{period}: texto y cuadro no concuerdan')
    return amount

def fetch_validated(session,period,url):
    response=session.get(url,headers=UA,timeout=70);response.raise_for_status()
    amount=read_official_pdf(response.content,period)
    return {'mes':period,'valor':amount,'fuente':url,'pdf':response.content}
