"""Copias de seguridad del archivo .MDB de Aniwin.

Solo copia (lectura del original). Nunca modifica ni borra el archivo de Aniwin.
"""

import logging
import re
import shutil
from datetime import datetime
from pathlib import Path

log = logging.getLogger(__name__)

EXTENSIONES_BLOQUEO = (".ldb", ".laccdb")
RE_COPIA = re.compile(r"_(\d{4})-(\d{2})-(\d{2})_(\d{4})$")


class ArchivoEnUso(RuntimeError):
    """Aniwin/Access tiene el archivo abierto; reintentar más tarde."""


def en_uso(mdb: Path) -> bool:
    return any(mdb.with_suffix(ext).exists() for ext in EXTENSIONES_BLOQUEO)


def hacer_copia(mdb: Path, carpeta_copias: Path, ahora: datetime | None = None) -> Path:
    """Copia `mdb` a `carpeta_copias` con fecha y hora en el nombre y verifica el tamaño."""
    if not mdb.is_file():
        raise FileNotFoundError(f"No existe la base de datos: {mdb}")
    if en_uso(mdb):
        raise ArchivoEnUso(f"{mdb.name} está en uso; se reintentará más tarde.")

    ahora = ahora or datetime.now()
    carpeta_copias.mkdir(parents=True, exist_ok=True)
    destino = carpeta_copias / f"{mdb.stem.strip()}_{ahora:%Y-%m-%d_%H%M}{mdb.suffix.lower()}"
    shutil.copy2(mdb, destino)

    if destino.stat().st_size != mdb.stat().st_size:
        destino.unlink()
        raise OSError("La copia no coincide en tamaño con el original; se ha descartado.")
    log.info("Copia creada: %s", destino)
    return destino


def _fecha_copia(ruta: Path) -> datetime | None:
    m = RE_COPIA.search(ruta.stem)
    if not m:
        return None
    a, mes, d, hm = m.groups()
    return datetime(int(a), int(mes), int(d), int(hm[:2]), int(hm[2:]))


def depurar(carpeta_copias: Path, diarias: int = 30, mensuales: int = 12) -> list[Path]:
    """Elimina copias antiguas conservando las `diarias` últimas y una por mes (`mensuales` meses).

    Solo toca archivos con el patrón `*_AAAA-MM-DD_HHMM.mdb` dentro de `carpeta_copias`.
    Devuelve las copias eliminadas.
    """
    copias = sorted(
        (c for c in carpeta_copias.glob("*.mdb") if _fecha_copia(c)),
        key=lambda c: _fecha_copia(c),
        reverse=True,
    )
    conservar = set(copias[:diarias])
    vistos_mes: set[tuple[int, int]] = set()
    for c in reversed(copias):  # la más antigua de cada mes
        f = _fecha_copia(c)
        clave = (f.year, f.month)
        if clave not in vistos_mes and len(vistos_mes) < mensuales:
            vistos_mes.add(clave)
            conservar.add(c)

    eliminadas = [c for c in copias if c not in conservar]
    for c in eliminadas:
        c.unlink()
        log.info("Copia antigua eliminada: %s", c)
    return eliminadas
