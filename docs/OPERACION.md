# Operación y publicación

## Ejecución

Python 3.12 y dependencias de `requirements-actions.txt`.

```bash
pip install -r requirements-actions.txt
python scripts/00_orquestador.py
python scripts/00_orquestador.py --actualizar
```

`00_orquestador.py` invoca en orden `01_descargar_fuentes.py`, `02_actualizar_excel.py`, `03_generar_html.py` y `04_validar.py`. Si falla cualquiera, no se ejecutan los pasos posteriores.

## Origen de datos

- `data/ipc_fuente.xlsx`: descarga oficial del IPC, archivo de entrada.
- `data/ipc_cba_actualizado.xlsx`: libro central. Las hojas `IPC series` y `CBA valores` alimentan el gráfico. Las demás hojas documentan composición, correspondencias y metodología.
- `site/plantilla.html`: estructura y lógica de interfaz sin cifras estadísticas definitivas.
- `site/index.html` y `data/cba_series.json`: derivados que se regeneran; no se editan como datos.

## Actualización monetaria oficial

Los nuevos valores publicados de la CBA deben contrastarse con el cuadro oficial del Ministerio e ingresarse en `CBA valores`, con mes, monto, condición `Oficial MDSF` y URL de origen. No se imputan automáticamente meses sin documentación. La retroproyección experimental se recalcula desde el valor oficial de referencia y el índice alimentario disponible. **No equivale al deflactor compuesto ministerial.**

## GitHub Actions

Habilitar `Settings > Pages > Source: GitHub Actions`, configurar permisos de lectura/escritura para Actions y ejecutar el workflow manualmente antes de activar el calendario. El workflow ejecuta `00_orquestador.py --actualizar`, registra archivos validados y despliega `site`. La acción no actualiza automáticamente montos CBA desde PDF; no atribuirle esa capacidad.

Si la descarga o las validaciones fallan, no hay despliegue. Revisar los registros, el Excel y las URLs de origen.

## Informes CBA

El script `01_descargar_fuentes.py --actualizar` identifica informes desde el catálogo oficial y verifica sus PDF. El script `02_actualizar_excel.py` vuelve a abrir cada PDF almacenado antes de incorporarlo al Excel. El manifiesto `data/cba_fuentes_validadas.json` registra mes, fuente, monto y SHA-256. Los documentos se guardan en `data/cba_informes/`.

Cuando se publique un nuevo informe, ejecutar el orquestador completo en un entorno con acceso a Internet. Ante cambios del formato del cuadro, fallos de descarga o revisiones de importes históricos, se debe revisar el error y el documento antes de repetir el workflow.
