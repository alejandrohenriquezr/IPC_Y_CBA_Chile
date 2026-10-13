"""Lectura estructurada de XLSX con la biblioteca estándar (sin alterar el libro)."""
from pathlib import Path
from zipfile import ZipFile
import re
import xml.etree.ElementTree as ET

NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}

def sheets(path):
    """Devuelve filas por nombre de hoja; resuelve cadenas compartidas y celdas vacías."""
    out={}
    with ZipFile(path) as z:
        shared=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            q=ET.fromstring(z.read('xl/sharedStrings.xml'))
            shared=[''.join(n.itertext()) for n in q.findall('m:si',NS)]
        book=ET.fromstring(z.read('xl/workbook.xml'))
        rels=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        paths={n.attrib['Id']:n.attrib['Target'] for n in rels}
        for sh in book.findall('.//m:sheet',NS):
            rid=sh.attrib.get('{'+NS['r']+'}id');target=paths[rid].lstrip('/')
            if not target.startswith('xl/'):target='xl/'+target
            doc=ET.fromstring(z.read(target));rows=[]
            for row in doc.findall('.//m:sheetData/m:row',NS):
                cells={}
                for c in row.findall('m:c',NS):
                    a=re.match(r'[A-Z]+',c.attrib['r']).group();idx=0
                    for ch in a:idx=idx*26+ord(ch)-64
                    v=c.find('m:v',NS)
                    if c.attrib.get('t')=='inlineStr':val=''.join(c.find('m:is',NS).itertext())
                    elif v is None:val=None
                    elif c.attrib.get('t')=='s':val=shared[int(v.text)]
                    elif c.attrib.get('t') in ('str','e'):val=v.text
                    else:
                        num=float(v.text);val=int(num) if num.is_integer() else num
                    cells[idx-1]=val
                if cells:rows.append([cells.get(i) for i in range(max(cells)+1)])
            out[sh.attrib['name']]=rows
    return out

def replace_sheets(path, changes):
    """Sustituye exclusivamente las hojas indicadas; preserva el resto del libro XLSX.

    Los datos se serializan en OOXML nativo. Se conservan hojas ajenas,
    relaciones, formatos y metadatos de otras partes del libro.
    """
    import os
    from tempfile import NamedTemporaryFile
    from zipfile import ZIP_DEFLATED
    M='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    ET.register_namespace('',M)
    with ZipFile(path) as source:
        book=ET.fromstring(source.read('xl/workbook.xml'))
        rels=ET.fromstring(source.read('xl/_rels/workbook.xml.rels'))
        paths={node.attrib['Id']:node.attrib['Target'] for node in rels}
        replace={}
        for sh in book.findall('.//m:sheet',NS):
            name=sh.attrib['name']
            if name not in changes:continue
            rid=sh.attrib['{'+NS['r']+'}id']
            target=paths[rid].lstrip('/')
            if not target.startswith('xl/'):target='xl/'+target
            replace[target]=changes[name]
        if set(changes)!=set(sh.attrib['name'] for sh in book.findall('.//m:sheet',NS) if sh.attrib['name'] in changes):
            raise ValueError('Hoja de destino no encontrada')
        with NamedTemporaryFile(suffix='.xlsx',delete=False,dir=Path(path).parent) as tmp:
            temp=Path(tmp.name)
        try:
            with ZipFile(temp,'w') as dest:
                for item in source.infolist():
                    if item.filename not in replace:
                        dest.writestr(item,source.read(item.filename));continue
                    sheet=ET.Element('{'+M+'}worksheet');body=ET.SubElement(sheet,'{'+M+'}sheetData')
                    for ri,values in enumerate(replace[item.filename],1):
                        row=ET.SubElement(body,'{'+M+'}row',{'r':str(ri)})
                        for ci,v in enumerate(values):
                            if v is None:continue
                            num=ci+1;col=''
                            while num: num,rem=divmod(num-1,26);col=chr(65+rem)+col
                            cell=ET.SubElement(row,'{'+M+'}c',{'r':f'{col}{ri}'})
                            if isinstance(v,(int,float)) and not isinstance(v,bool):
                                ET.SubElement(cell,'{'+M+'}v').text=str(v)
                            else:
                                cell.set('t','inlineStr');ET.SubElement(ET.SubElement(cell,'{'+M+'}is'),'{'+M+'}t').text=str(v)
                    dest.writestr(item,ET.tostring(sheet,encoding='utf-8',xml_declaration=True))
            temp.replace(path)
        finally:
            temp.unlink(missing_ok=True)
