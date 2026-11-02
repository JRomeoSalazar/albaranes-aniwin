"""Ajuste de texto a líneas de longitud máxima (90 caracteres en Aniwin)."""

import textwrap

MAX_CHARS_DEFECTO = 90


def ajustar(texto: str, ancho: int = MAX_CHARS_DEFECTO) -> list[str]:
    """Divide `texto` en líneas de como máximo `ancho` caracteres.

    - No corta palabras salvo que una palabra sola supere el ancho.
    - Respeta los saltos de línea existentes (cada párrafo se ajusta por separado).
    - Las líneas vacías se conservan como separador.
    """
    lineas: list[str] = []
    for parrafo in texto.splitlines():
        if not parrafo.strip():
            lineas.append("")
            continue
        lineas.extend(
            textwrap.wrap(
                parrafo.strip(),
                width=ancho,
                break_long_words=True,
                break_on_hyphens=False,
            )
        )
    return lineas
