"""Ejecución principal (Fase 1): notas -> texto listo para pegar en Aniwin.

Uso:
    python -m albaranes.main [--config config.ini] [--dry-run]

Origen provisional: carpeta con archivos .txt. El origen real está pendiente de decidir.
"""

import argparse
import configparser
import logging
import shutil
import sys
from pathlib import Path

from .parser import Nota, NotaInvalida, interpretar
from .wrap import ajustar

log = logging.getLogger("albaranes")


def formatear_salida(nota: Nota, ancho: int) -> str:
    """Texto listo para pegar en la descripción de Aniwin."""
    partes = [f"Albarán {nota.numero} - {nota.cliente}"]
    for titulo, contenido in (
        ("REPUESTOS", nota.repuestos),
        ("TRABAJOS REALIZADOS", nota.trabajos),
        ("RECOMENDACIONES", nota.recomendaciones),
    ):
        if contenido:
            partes.append("")
            partes.append(f"{titulo}:")
            partes.extend(ajustar(contenido, ancho))
    return "\n".join(partes) + "\n"


def procesar_carpeta(cfg: configparser.ConfigParser, dry_run: bool) -> int:
    ancho = cfg.getint("general", "max_chars_linea", fallback=90)
    entrada = Path(cfg.get("origen", "carpeta_entrada"))
    procesadas = Path(cfg.get("origen", "carpeta_procesadas"))
    errores = Path(cfg.get("origen", "carpeta_errores"))
    salida = Path(cfg.get("salida", "carpeta_salida"))

    if not dry_run:
        for c in (procesadas, errores, salida):
            c.mkdir(parents=True, exist_ok=True)

    fallos = 0
    for ruta in sorted(entrada.glob("*.txt")):
        try:
            nota = interpretar(ruta.read_text(encoding="utf-8"))
            texto = formatear_salida(nota, ancho)
            for aviso in nota.avisos:
                log.warning("%s: %s", ruta.name, aviso)
            if dry_run:
                print(f"--- {ruta.name} ---\n{texto}")
            else:
                (salida / f"albaran_{nota.numero}.txt").write_text(texto, encoding="utf-8")
                shutil.move(str(ruta), procesadas / ruta.name)
            log.info("Procesada: %s (albarán %s)", ruta.name, nota.numero)
        except NotaInvalida as e:
            fallos += 1
            log.error("Error en %s: %s", ruta.name, e)
            if not dry_run:
                shutil.move(str(ruta), errores / ruta.name)
    return fallos


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", default="config.ini")
    p.add_argument("--dry-run", action="store_true", help="No mueve ni escribe archivos; muestra el resultado.")
    args = p.parse_args(argv)

    cfg = configparser.ConfigParser()
    if not cfg.read(args.config, encoding="utf-8"):
        print(f"No se encuentra {args.config}. Copia config.example.ini a config.ini.", file=sys.stderr)
        return 2

    log_dir = Path(cfg.get("general", "log_dir", fallback="logs"))
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(log_dir / "albaranes.log", encoding="utf-8"), logging.StreamHandler()],
    )

    tipo = cfg.get("origen", "tipo", fallback="carpeta")
    if tipo != "carpeta":
        log.error("Origen '%s' aún no implementado (pendiente de decidir).", tipo)
        return 2
    return 1 if procesar_carpeta(cfg, args.dry_run) else 0


if __name__ == "__main__":
    sys.exit(main())
