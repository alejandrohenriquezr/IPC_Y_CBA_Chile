"""Agrega al README la descripción estadística de incidencias sin alterar otras secciones."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
README=ROOT/'README.md'
MARK='## Incidencias y contribuciones'
TEXT='''## Incidencias y contribuciones

El ranking permite alternar entre **variaciones (%)** e **incidencias /
contribuciones (puntos porcentuales)**. Para IPC completo se utilizan las
incidencias mensuales, acumuladas anuales y a doce meses publicadas por el INE.
No se interpreta la variación desde enero de 2024 como incidencia oficial.

En productos vinculados a la CBA, las contribuciones son una **estimación
analítica del cambio de costo del subtotal homologado**, no incidencias de la
serie monetaria oficial. Los cálculos se conservan en las hojas `IPC incidencias`
y `CBA incidencias estimadas` del libro principal.

Consultar [Metodología](docs/METODOLOGIA.md) y
[Correspondencias](docs/CORRESPONDENCIAS.md).
'''
def main():
    content=README.read_text(encoding='utf-8')
    if MARK not in content:
        README.write_text(content.rstrip()+'\n\n'+TEXT,encoding='utf-8')
if __name__=='__main__':main()
