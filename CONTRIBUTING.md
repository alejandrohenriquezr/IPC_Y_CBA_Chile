# Contribuciones

IPC y CBA Chile acepta reportes de errores, propuestas documentadas y
contribuciones de código mediante GitHub Issues y Pull Requests.

## Flujo de contribución

1. Revisar los Issues existentes y abrir uno cuando el cambio afecte
   definiciones estadísticas, datos, correspondencias CBA–IPC o la interfaz.
2. Crear una rama a partir de `main` y realizar cambios acotados.
3. Si se modifican cálculos, actualizar las pruebas en `tests/`.
4. Ejecutar `python -m unittest discover -s tests -v` y
   `python scripts/04_validar.py` cuando las dependencias estén instaladas.
5. Abrir un Pull Request describiendo el cambio, sus fuentes, las pruebas
   ejecutadas y, si procede, capturas del resultado.
6. No incluir credenciales, datos personales, contenido de terceros sin
   autorización ni cifras atribuidas a una fuente sin respaldo verificable.

Las cifras del IPC y la CBA se actualizan mediante los procesos documentados
en el repositorio. No editar directamente los valores generados en el HTML;
las transformaciones deben poder reproducirse a partir del Excel y los scripts.

## Derechos sobre las contribuciones

Las contribuciones de código y documentación original propuestas para
incorporación al proyecto se ofrecen bajo Apache License 2.0, de acuerdo con
su sección 5, sin cesión adicional de titularidad.

Se utiliza el Developer Certificate of Origin (DCO 1.1). Al contribuir,
se declara que se tiene derecho a enviar el cambio bajo la licencia del
proyecto. Los commits de aportes externos deben llevar la línea:

```text
Signed-off-by: Nombre Apellido <correo@example.com>
```

Para incorporarla automáticamente al crear un commit:
`git commit -s -m "Descripción del cambio"`.

Texto y detalles del DCO: https://developercertificate.org/

La aceptación de un Pull Request queda sujeta a la revisión de su corrección
técnica, trazabilidad de fuentes y compatibilidad de licencias. No se exige
ceder los derechos patrimoniales al responsable del repositorio.

## Conducta y comunicación

Consultar `CODE_OF_CONDUCT.md`. Para reportes ordinarios usar Issues.
Para comunicaciones privadas sobre conducta, utilizar el correo de contacto
indicado en `AUTHORS.md`.
