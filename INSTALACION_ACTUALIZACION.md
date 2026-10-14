# Instalación de actualización de incidencias

Aplicar el contenido del ZIP sobre una copia actualizada del repositorio
`IPC_Y_CBA_Chile`, preservando los demás archivos, incluidos `LICENSE`,
`NOTICE`, `CONTRIBUTING.md` y `AUTHORS.md`.

En PowerShell, desde la carpeta del repositorio:

```powershell
# Descargar cambios previos y conservar cualquier cambio local.
git status
git pull --ff-only origin main

# Extraer los archivos del parche sobre el repositorio.
Expand-Archive -Path 'C:\ruta\cba_ipc_incidencias_parche.zip' -DestinationPath . -Force

# Completar la documentación principal sin sustituir secciones anteriores.
py scripts/actualizar_readme_incidencias.py

# Pruebas estadísticas, generación local y validación.
py -m unittest discover -s tests -v
py scripts/00_orquestador.py
py scripts/04_validar.py

git status
git add scripts docs tests site data/ipc_cba_actualizado.xlsx README.md
git commit -m 'Incorporar incidencias IPC y contribuciones estimadas CBA'
git push origin main
```

El proceso regenerará HTML y JSON derivados desde el Excel, por lo que no se
editan cifras incrustadas en el código. La publicación automática en Pages
reutiliza los pasos del workflow existentes.

La prueba visual automatizada no pudo ejecutarse en este entorno; antes de
publicar conviene comprobar en el navegador el selector, la animación y las
exportaciones en ambos universos.
