# CBA e IPC de Chile: evolución y ranking de productos

**Autor:** Alejandro Henríquez  
**Contacto:** [alejandro.henriquezr@hotmail.com](mailto:alejandro.henriquezr@hotmail.com)  
**Perfil profesional:** [LinkedIn](https://www.linkedin.com/in/alejandro-henríquez-rodríguez-baab18358)  
**Versión:** 1.0.0

Visualización de la **Canasta Básica de Alimentos (CBA, metodología 2024)** y de los índices de precios al consumidor (IPC, base anual 2023=100).

## Abrir las visualizaciones

- [Visualización para GitHub Pages](site/index.html) (tras habilitar Pages: `https://alejandrohenriquezr.github.io/IPC_Y_CBA_Chile/`).
- [Libro analítico actualizado](data/ipc_cba_actualizado.xlsx).
- [Composición y correspondencias](data/ipc_cba_actualizado.xlsx), hojas `CBA 2024` y `Correspondencias`.

La vista monetaria distingue **valores monetarios oficiales CBA** (enero–agosto de 2026 en el conjunto de datos incluido) y **estimación retrospectiva experimental** (enero 2024–diciembre 2025). La segunda presenta el ranking por variación acumulada desde enero de 2024 de los productos IPC vinculados analíticamente a la CBA. No se suman los índices por producto para construir el valor oficial.

**Advertencia metodológica:** la estimación retrospectiva inicial usa solamente el IPC de la división 1, debido a que no se ha incorporado la serie y ponderadores operativos del deflactor oficial compuesto, que además incluye alimentos consumidos fuera del hogar. **No es una serie oficial ni una aplicación íntegra de la metodología del Ministerio.** Véase [metodología](docs/METODOLOGIA.md).

## Estructura

| Ruta | Función |
|---|---|
| `site/index.html` | Web estática autónoma; GitHub Pages publica esta carpeta |
| `data/ipc_cba_actualizado.xlsx` | Excel de análisis con composición y dos tramos de serie |
| `data/cba_series.json` | Serie monetaria, procedencia y separación oficial/estimada |
| `data/ipc_fuente.xlsx` | Archivo IPC oficial descargado y verificado |
| `scripts/00_orquestador.py` | Coordina descarga, actualización de Excel, HTML y validación |
| `scripts/04_validar.py` | Verificación de datos y controles antes de publicar |
| `.github/workflows/actualizar-publicar.yml` | Action de actualización y Pages |
| `docs/METODOLOGIA.md` | Fórmulas, límites y fuentes |
| `docs/CORRESPONDENCIAS.md` | Regla de emparejamiento CBA–IPC |
| `docs/OPERACION.md` | Instalación, configuración, errores y publicación |

## Puesta en marcha

1. Mantener el contenido del repositorio, incluidos `.github/workflows` y la carpeta `site`.
2. En **Settings > Pages > Build and deployment**, seleccionar **Source: GitHub Actions**.
3. En **Settings > Actions > General**, autorizar al workflow para escribir en el repositorio si corresponde y permitir la publicación Pages.
4. Ejecutar **Actions > Actualizar IPC, CBA y publicar Pages > Run workflow**. Si cambia el formato de los PDF oficiales, el proceso se detiene y se aplica el procedimiento de contingencia descrito en [operación](docs/OPERACION.md).
5. Verificar `https://alejandrohenriquezr.github.io/IPC_Y_CBA_Chile/` y comparar contra la tabla `data/cba_series.json`.

La publicación requiere verificar los datos y la extracción de los informes mensuales. Ante fallas de extracción, se conserva la última versión validada.

## Fuentes y atribución

La visualización monetaria identifica los informes de la CBA del Ministerio de Desarrollo Social y Familia y, para el tramo estimado, las series del IPC del Instituto Nacional de Estadísticas. El ranking por productos utiliza los índices del INE y la composición CBA publicada por el Ministerio. Las notas de cada gráfico detallan la fuente aplicable; las referencias documentales completas se encuentran en [Metodología](docs/METODOLOGIA.md).

## Integridad de datos

- Los datos oficiales monetarios están distinguidos de los estimados.
- Las correspondencias CBA–IPC son analíticas, no una homologación oficial exhaustiva.
- Los artefactos publicados se someten a controles automáticos y contrastes con los informes en PDF.
- No corresponde describir la retroproyección mediante IPC división 1 como «deflactor oficial».

## Licencia y contribuciones

Copyright 2026 Alejandro Henríquez. El código y la documentación originales
se distribuyen bajo [Apache License 2.0](LICENSE); los avisos de atribución
figuran en [NOTICE](NOTICE). La licencia del software no reemplaza las
condiciones aplicables a las fuentes estadísticas de terceros.

Los datos del INE se rigen por sus términos de uso y la licencia CC BY-SA 4.0.
Los materiales del Ministerio de Desarrollo Social y Familia mantienen sus
propias condiciones. Las fuentes y el tratamiento de datos transformados se
describen en [Licencias y procedencia de datos](docs/LICENCIAS_DATOS.md).

Las contribuciones se gestionan mediante Issues y Pull Requests, conforme a
[CONTRIBUTING.md](CONTRIBUTING.md) y al
[Código de conducta](CODE_OF_CONDUCT.md). Los cambios deben conservar
trazabilidad estadística y ser compatibles con las licencias aplicables.

Este es un proyecto independiente; sus correspondencias, visualizaciones
y estimaciones no constituyen publicaciones oficiales ni implican respaldo
institucional del INE o del Ministerio.

## Visualización CBA en pesos y variaciones

La vista CBA dispone de selector **Valor ($) / Variación acumulada (%)** y período de referencia: enero de 2024, enero del año seleccionado o últimos 12 meses. Las variaciones se calculan a partir de valores monetarios del libro, y no de la suma de variaciones individuales de productos. El tramo histórico estimado utiliza IPC de alimentos como proxy, no el deflactor compuesto oficial. La comprobación `python scripts/04_validar.py` verifica que los controles se conservan después de regenerar la página.

## Secuencia de ejecución y fuente única de datos

`python scripts/00_orquestador.py` utiliza los archivos locales. Con `--actualizar` descarga el Excel oficial del IPC. El orden es: `01_descargar_fuentes.py`, `02_actualizar_excel.py`, `03_generar_html.py`, `04_validar.py`. El sitio `site/index.html` se regenera desde `site/plantilla.html` y las hojas **IPC series** y **CBA valores** del libro `data/ipc_cba_actualizado.xlsx`. No se editan datos directamente en el HTML ni en archivos JSON.

La hoja **CBA valores** contiene las cifras oficiales contrastadas con sus documentos de origen y el tramo experimental calculado. Los importes oficiales nuevos se recuperan y contrastan desde los PDF ministeriales mediante el extractor. Si la comprobación no es inequívoca, se detiene la actualización. Se detiene ante fallas de estructura o series incompletas. `data/cba_series.json` es un resultado derivado, no una segunda fuente de verdad. La hoja **IPC series** conserva la asignación `CBA=1` para los productos homologados; se revisa ante modificaciones de clasificación.

## Actualización automatizada de la CBA oficial

La ejecución `python scripts/00_orquestador.py --actualizar` comprueba la fuente IPC y consulta el catálogo del [Observatorio Social](https://observatorio.ministeriodesarrollosocial.gob.cl/nueva-serie-cba-2026). Los informes identificados se descargan y validan como documentos de la metodología 2024. Se extrae exclusivamente la fila `CBA` del Cuadro 1 (página impresa 5, quinta página del PDF) y se contrasta el período y el monto cuando exista repetición narrativa. El valor se registra en `CBA valores`, con URL del informe; los PDF y su manifiesto se conservan como respaldo.

Si el informe cambia de estructura, hay discrepancia con el histórico, el IPC aún no cubre el mes de la CBA o falla una fuente, **el proceso interrumpe la publicación**. Los datos oficiales existentes no se reemplazan por estimaciones. El modo sin `--actualizar` utiliza los datos y fuentes locales sin efectuar consultas externas.

La comprobación de la extracción debe realizarse al incorporar un nuevo formato de informe; la detección automatizada no constituye verificación editorial independiente.

### Ranking de variaciones del IPC

La vista de productos ofrece un selector para las variaciones **mensual**, **12 meses**, **acumulada anual** (respecto de diciembre anterior) y **desde enero de 2024** (respecto de enero de 2024). Los botones **▲ Mayores** y **▼ Menores** invierten el orden del ranking. «Menores» incluye variaciones negativas si existen; si todas son positivas, identifica los menores aumentos.

Las series de la hoja `IPC series` contienen variaciones porcentuales relativas a enero de 2024. El gráfico recupera matemáticamente las variaciones entre fechas usando la razón `(100 + variación_t) / (100 + variación_referencia) - 1`. No se completan referencias faltantes: enero de 2024 no dispone de diciembre de 2023 para la variación acumulada anual y los primeros doce meses no disponen del mismo mes anterior para la variación interanual.

El modo «Productos vinculados a la CBA» fija el nivel Producto y oculta los controles de nivel y división, manteniendo los filtros de variación, sentido y número de barras. La exportación CSV y la animación utilizan la variación seleccionada.

## Versión 1.0: validación y publicación

El orquestador usa una copia temporal; si descarga, extracción, transformación o validación falla, no promueve nuevos archivos locales. Las series IPC se identifican por sus códigos jerárquicos oficiales, no por glosas. La publicación Pages se ejecuta en un trabajo separado, solo tras superar la construcción y las pruebas. Consultar [validación de la versión 1.0](docs/VALIDACION_1_0.md).

### Cobertura y estado de actualización

La cobertura vigente y fecha de generación se almacenan en [`data/estado_actualizacion.json`](data/estado_actualizacion.json). Este archivo se genera desde el Excel en cada ejecución válida, evitando mantener fechas de corte manualmente en el README.

### Navegación jerárquica del IPC

En el universo **IPC completo**, cada barra permite consultar las categorías del nivel inferior siguiendo los códigos oficiales de clasificación: División → Grupo → Clase → Subclase → Producto. La ruta seleccionada se presenta como una miga de pan; cada uno de sus enlaces permite regresar a un nivel anterior. Los filtros de período, sentido de ordenamiento y cantidad de categorías se conservan durante la navegación. Al cambiar de universo, división o nivel inicial, la ruta se restablece.

La navegación utiliza los códigos jerárquicos contenidos en `data/ipc_cba_actualizado.xlsx` y se genera mediante `scripts/03_generar_html.py` a partir de `site/plantilla.html`. El universo **Productos vinculados a la CBA** está definido directamente a nivel Producto y no presenta categorías descendientes.
