"""Orquesta sobre copia aislada; promueve artefactos únicamente tras validar."""
import argparse, subprocess, sys, tempfile, shutil, os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES=['data/ipc_fuente.xlsx','data/ipc_cba_actualizado.xlsx','data/cba_series.json',
       'data/cba_fuentes_validadas.json','site/index.html','data/estado_actualizacion.json']
def main():
    p=argparse.ArgumentParser();p.add_argument('--actualizar',action='store_true');args=p.parse_args()
    # Copia separada: ninguna etapa puede escribir en los artefactos publicados.
    with tempfile.TemporaryDirectory(prefix='cba-ipc-stage-') as td:
        root=Path(td)/'repo'
        shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('__pycache__','.git'))
        stages=['01_descargar_fuentes.py','02_actualizar_excel.py','03_generar_html.py','04_validar.py']
        for name in stages:
            cmd=[sys.executable,str(root/'scripts'/name)]
            if name=='01_descargar_fuentes.py' and args.actualizar:cmd.append('--actualizar')
            print('Ejecutando',name,flush=True)
            subprocess.run(cmd,cwd=root,check=True)
        # Se han validado todas las salidas antes de tocar el directorio estable.
        # La publicación remota es atómica en GitHub Pages: se despliega el artefacto completo.
        staged=[(root/p,ROOT/p) for p in FILES if (root/p).is_file()]
        staged += [(f,ROOT/'data/cba_informes'/f.name) for f in (root/'data/cba_informes').glob('*.pdf')] if (root/'data/cba_informes').is_dir() else []
        for source,target in staged:
            target.parent.mkdir(parents=True,exist_ok=True)
            tmp=target.with_name(target.name+'.new')
            shutil.copy2(source,tmp);os.replace(tmp,target)
        print('Datos validados y promovidos:',len(staged))
if __name__=='__main__':main()
