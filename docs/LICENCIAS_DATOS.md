# Licencias y procedencia de los datos

Este repositorio combina software y documentación originales con datos
estadísticos de terceros. La licencia Apache 2.0 del código del proyecto
**no sustituye** las condiciones de las fuentes originales.

## Código y documentación del proyecto

Copyright 2026 Alejandro Henríquez.

El código original Python y JavaScript, y la documentación de elaboración
propia, se distribuyen bajo Apache License, Version 2.0
([LICENSE](../LICENSE)). Se conservan los avisos de [NOTICE](../NOTICE).

## IPC: Instituto Nacional de Estadísticas (INE), Chile

- Fuente: Índice de Precios al Consumidor (IPC), base anual 2023=100.
- Serie utilizada: https://www.ine.gob.cl/docs/default-source/%C3%ADndice-de-precios-al-consumidor/cuadros-estadisticos/base-anual-2023_100/series-de-tiempo/ipc-xls.xlsx
- Términos del INE: https://www.ine.gob.cl/terminos-de-uso-y-licencia-de-datos-abiertos
- Licencia declarada por el INE: Creative Commons Atribución-CompartirIgual
  4.0 Internacional (CC BY-SA 4.0):
  https://creativecommons.org/licenses/by-sa/4.0/deed.es

Para reutilizar datos del INE, se debe citar la fuente, enlazar la licencia
e indicar las transformaciones efectuadas. Si se distribuye una adaptación
sujeta a la condición CompartirIgual, se deben respetar sus obligaciones.

Los libros procesados, series transformadas y gráficos requieren evaluar la
aplicación de esas condiciones al contenido estadístico. No deben interpretarse
como una publicación oficial del INE.

## CBA: Ministerio de Desarrollo Social y Familia, Observatorio Social

- Fuente: Canasta Básica de Alimentos (CBA), metodología 2024.
- Informes: https://observatorio.ministeriodesarrollosocial.gob.cl/nueva-serie-cba-2026
- Metodología: https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Metodologia_de_Medicion_de_la_Pobreza_por_Ingresos_2024.pdf

La reproducción de textos, cuadros, tablas o documentos del Observatorio
debe respetar las condiciones que correspondan a cada fuente.
**No se atribuye aquí una licencia Creative Commons ni otra licencia
específica al Ministerio sin verificarla para ese material.**

## Transformaciones y advertencias

Las correspondencias CBA–IPC son elaboraciones analíticas y no una
homologación oficial integral. Las variaciones y rankings se calculan sobre
series del IPC. La retroproyección histórica del valor CBA es una estimación
experimental basada en un indicador aproximado, diferenciada de los valores
oficiales publicados.

Fórmulas y procedimientos: [METODOLOGIA.md](METODOLOGIA.md).

## Créditos sugeridos

- Índices y rankings: «Fuente: Elaboración propia en base a información del
  Instituto Nacional de Estadísticas (INE), IPC base anual 2023=100».
- Valor monetario oficial de la CBA: «Fuente: Elaboración propia en base a
  información del Ministerio de Desarrollo Social y Familia, Observatorio
  Social, Canasta Básica de Alimentos».
- Retroproyección experimental: «Fuente: Elaboración propia en base a
  información del Ministerio de Desarrollo Social y Familia y del INE,
  IPC base anual 2023=100. Retroproyección experimental».

La atribución de fuentes no implica patrocinio, validación o respaldo
institucional de los resultados del proyecto.
