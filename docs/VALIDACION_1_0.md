# Validación de la versión 1.0

- La ejecución del orquestador procesa en un directorio temporal y promueve resultados solo tras pasar los controles.
- Identificación IPC: códigos jerárquicos oficiales de división/grupo/clase/subclase/producto; se conserva la clasificación analítica CBA por código.
- Las pruebas de fórmulas no sustituyen el contraste independiente con datos publicados.
- La extracción de PDF exige concordancia entre período, metodología y valor CBA; un cambio de estructura bloquea la publicación.
- Los archivos antiguos en Pages no se reemplazan si falla el job de construcción.
- El dato oficial de CBA se distingue de la retroproyección experimental basada en IPC división 1. No equivale al deflactor ministerial compuesto.
- La ejecución completa en GitHub Actions y la primera descarga real de nuevos informes siguen pendientes de prueba en el repositorio de destino.

## Ejecución

```bash
python -m unittest discover -s tests -v
python scripts/00_orquestador.py
python scripts/04_validar.py
```
