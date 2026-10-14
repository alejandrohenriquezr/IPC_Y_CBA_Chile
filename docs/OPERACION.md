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


## Actualización de incidencias

El proceso secuencial incorpora `02b_actualizar_incidencias.py` después de
`02_actualizar_excel.py`. Utiliza las columnas de incidencia y ponderación
del archivo oficial del IPC para completar la hoja `IPC incidencias`, y los
gastos y correspondencias de la CBA para `CBA incidencias estimadas`.
Los datos experimentales se validan sin sustituir incidencias oficiales.

El selector de incidencias en el universo IPC admite mensual, acumulada anual
y doce meses. Para el origen enero de 2024 no se ofrece una incidencia oficial
reconstruida. En el universo CBA, se calcula la contribución respecto del
período seleccionado sobre el subtotal vinculado, en puntos porcentuales.

## Velocidad de reproducción y exportación

La animación del ranking utiliza 1,6 segundos por mes a velocidad 1×. El control de
velocidad de la interfaz permite 0,75×, 1×, 1,25× y 1,5×; modifica la cadencia
mensual y la duración de las transiciones. Durante la reproducción, cambiar
la velocidad no modifica la selección de fecha ni reinicia la serie.

Las exportaciones animadas GIF y video se generan siempre a velocidad 1×
(1,6 segundos por transición mensual), independientemente de la velocidad
seleccionada para reproducir el gráfico. La exportación de MP4 depende del
soporte del navegador para MediaRecorder.

## Escala horizontal del ranking

El eje horizontal utiliza un dominio fijo para cada combinación de universo,
indicador, período, nivel y selección jerárquica. Los límites se obtienen de las
categorías elegibles durante todos los meses disponibles; se mantiene el cero
y se agrega un margen del 10 % a los extremos distintos de cero. Los límites
no dependen del mes reproducido ni del orden de mayor o menor incidencia o
variación. Las exportaciones PNG, GIF y video utilizan el mismo dominio que
el gráfico interactivo. Al cambiar de filtros o de ruta jerárquica se calcula
un nuevo dominio.

## Valores en barras y cobertura de períodos

El ranking presenta el valor seleccionado junto al extremo de cada barra: a la derecha
para valores positivos y a la izquierda para valores negativos. Las variaciones se
expresan en porcentaje (%) y las incidencias o contribuciones en puntos porcentuales
(p.p.). Las exportaciones de imagen y video utilizan las mismas unidades.

El control de tiempo comienza en el primer período con una comparación válida:
- Desde enero de 2024: febrero de 2024.
- Mensual: febrero de 2024.
- A doce meses: enero de 2025.
- Acumulada en el año: enero de 2025, cuando está disponible diciembre de 2024.

Si cambia el indicador o el período de comparación, se actualiza el límite inicial
del selector temporal. La reproducción y las exportaciones animadas omiten los meses
anteriores a ese límite. Si cambian las fuentes, el cálculo del primer mes disponible
se realiza a partir de las series efectivamente presentes, no de fechas fijas.


## Documentación pública en HTML

La carpeta `site/documentacion` incluye cinco páginas de lectura con una navegación común implementada mediante `site/assets/navegacion.css` y `site/assets/navegacion.js`. El panel documental se abre dentro de la página principal, conservando el estado temporal y los filtros del visualizador; cada página también funciona por su URL independiente. Los enlaces a descargas internas se resuelven dentro de la carpeta publicada `site/datos`. El generador actualiza las copias del libro y la cobertura en el sitio en cada construcción validada.
