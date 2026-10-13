# Metodología y fuentes

## Qué representan los datos

**Montos oficiales:** Canasta Básica de Alimentos (CBA) metodología 2024, valores monetarios mensuales publicados por el Ministerio de Desarrollo Social y Familia. Primera publicación bajo esta serie en 2026.

**Montos retroproyectados:** estimación experimental de qué costo habría tenido el valor de enero de 2026 trasladado hacia atrás mediante las variaciones del índice de la división 1 del IPC base 2023=100.

**Ranking de productos:** variación de cada producto IPC respecto de su propio índice de enero 2024, con filtro de correspondencias analíticas CBA–IPC. No se presenta como gasto ni contribución a la canasta oficial.

## Fórmulas implementadas

Sea `A=89.570 CLP` (enero 2026, ancla oficial), `F_t` el índice oficial de la división Alimentos y bebidas no alcohólicas del IPC, y `F_A` el correspondiente a enero 2026:

`CBA_proxy_t = A × F_t / F_A`, para enero 2024–diciembre 2025.

`Variación_producto_i,t = (IPC_producto_i,t / IPC_producto_i,2024-01 - 1) × 100`.

La aproximación por división 1 **no replica** el deflactor oficial de actualización de la CBA. La metodología del Ministerio considera alimentos dentro y fuera del hogar; un retrocálculo exacto exige el índice compuesto y los ponderadores empleados en cada período. Si se obtienen, corresponde sustituir el proxy y mantener una serie de control paralela.

No se empalman directamente valores de la metodología 2013 con los de 2024.

## Restricciones de publicación

- Mostrar tramo retroproyectado con línea discontinua, leyenda «Estimación experimental» y fuente IPC / ancla ministerial.
- Mostrar valores publicados con línea continua y leyenda «Oficial».
- Validar que las variaciones calculadas con valores redondeados pueden diferir de la variación oficial comunicada.
- No deducir precios de productos a partir de índices ni sumar índices no ponderados para inferir el valor de CBA.
- Si cambian definiciones, base IPC o informes del Ministerio, suspender la actualización y documentar el corte.

## Fuentes y páginas

1. **Ministerio de Desarrollo Social y Familia (2026)**, *Metodología de Medición de la Pobreza por Ingresos en Chile. Actualización 2024*, sección 2.9, p. 31 (deflactor), y anexo 6.2, pp. 42–44 (composición, cantidades y gasto). https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Metodologia_de_Medicion_de_la_Pobreza_por_Ingresos_2024.pdf
2. **Ministerio de Desarrollo Social y Familia**, *Valor de la Canasta Básica de Alimentos y Líneas de Pobreza*, informes mensuales 2026, cuadro 1, p. 5 (montos). https://observatorio.ministeriodesarrollosocial.gob.cl/nueva-serie-cba-2026
3. **INE**, *Índice de Precios al Consumidor, base anual 2023=100. Series de tiempo*, hoja `IPC 2023=100`, sin paginación (índices mensuales por nivel). https://www.ine.gob.cl/docs/default-source/%C3%ADndice-de-precios-al-consumidor/cuadros-estadisticos/base-anual-2023_100/series-de-tiempo/ipc-xls.xlsx

## Atribución por conjunto de datos

Los gráficos monetarios identifican al Ministerio de Desarrollo Social y Familia como fuente de los valores publicados y al INE como fuente del índice empleado en la estimación histórica. El ranking de productos utiliza las series del IPC del INE y la composición de la CBA documentada por el Ministerio. Las leyendas distinguen expresamente los valores oficiales de las estimaciones experimentales.


## Trazabilidad computacional

El libro `data/ipc_cba_actualizado.xlsx` es la fuente de las cifras del gráfico. `IPC series` contiene variaciones acumuladas desde enero de 2024 calculadas a partir de los índices de la fuente IPC; `CBA valores` distingue los importes publicados y las estimaciones retrospectivas. El proceso actualiza la estimación experimental usando el cociente de índices de la división 1 y el primer valor oficial CBA del libro. Ni el HTML ni el código Python contienen importes estadísticos de referencia fijos. Los períodos históricos no deben presentarse como resultados oficiales.


### Criterios de variación del ranking

Para cada categoría, la hoja `IPC series` conserva `v_t`, variación (%) del índice respecto de enero de 2024. La variación porcentual entre el período de referencia `r` y el mes `t` se obtiene mediante `100 × [(100 + v_t)/(100 + v_r) − 1]`. Las referencias disponibles son: mes anterior, mismo mes doce meses atrás, diciembre del año anterior y enero de 2024. Se excluyen del ranking las observaciones cuyo período de referencia no existe en la serie. El sentido del ordenamiento no altera la medida: ▲ ordena de mayor a menor; ▼ ordena de menor a mayor, incluidas tasas negativas.
