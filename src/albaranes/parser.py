"""Extracción de datos de una nota de albarán.

El formato real de la nota completa NO está confirmado (ver docs/02-aspectos-abiertos.md).
Este parser asume, a partir de lo visto en captura:

    Albarán XXXX - Nombre cliente
    Fecha: DD/MM/AAAA | Hora: HH:MM | Albarán Nº: XXXX
    Cliente: Nombre cliente
    Vehículo: ...

    Repuestos:
    ...
    Trabajos realizados:
    ...
    Recomendaciones:
    ...
"""

import re
from dataclasses import dataclass, field

SECCIONES = {
    "repuestos": "repuestos",
    "trabajos realizados": "trabajos",
    "trabajos": "trabajos",
    "recomendaciones": "recomendaciones",
}

RE_TITULO = re.compile(r"^\s*Albar[aá]n\s+(?P<num>\S+)\s*-\s*(?P<cliente>.+?)\s*$", re.IGNORECASE)
RE_FECHA = re.compile(r"Fecha:\s*(?P<fecha>\d{1,2}/\d{1,2}/\d{4})", re.IGNORECASE)
RE_HORA = re.compile(r"Hora:\s*(?P<hora>\d{1,2}:\d{2})", re.IGNORECASE)
RE_NUM = re.compile(r"Albar[aá]n\s*N[º°o]?\s*:\s*(?P<num>[\w.-]+)", re.IGNORECASE)
RE_CAMPO = re.compile(r"^\s*(?P<campo>Cliente|Veh[ií]culo)\s*:\s*(?P<valor>.*)$", re.IGNORECASE)
RE_SECCION = re.compile(r"^\s*(?P<nombre>[A-Za-zÁÉÍÓÚáéíóúñÑ ]+?)\s*:\s*(?P<resto>.*)$")


class NotaInvalida(ValueError):
    """La nota no tiene el formato esperado."""


@dataclass
class Nota:
    numero: str
    cliente: str
    fecha: str = ""
    hora: str = ""
    vehiculo: str = ""
    repuestos: str = ""
    trabajos: str = ""
    recomendaciones: str = ""
    avisos: list[str] = field(default_factory=list)


def interpretar(texto: str) -> Nota:
    """Convierte el texto de una nota en una `Nota`. Lanza `NotaInvalida` si falta el nº de albarán."""
    numero = ""
    cliente = ""
    fecha = hora = vehiculo = ""
    secciones: dict[str, list[str]] = {"repuestos": [], "trabajos": [], "recomendaciones": []}
    actual: str | None = None

    for linea in texto.splitlines():
        m = RE_TITULO.match(linea)
        if m and not numero:
            numero, cliente = m["num"], m["cliente"]
            continue

        if (m := RE_FECHA.search(linea)):
            fecha = m["fecha"]
            if (h := RE_HORA.search(linea)):
                hora = h["hora"]
            if (n := RE_NUM.search(linea)):
                numero = n["num"]
            continue

        if (m := RE_CAMPO.match(linea)):
            if m["campo"].lower() == "cliente":
                cliente = m["valor"].strip() or cliente
            else:
                vehiculo = m["valor"].strip()
            continue

        m = RE_SECCION.match(linea)
        if m and m["nombre"].strip().lower() in SECCIONES:
            actual = SECCIONES[m["nombre"].strip().lower()]
            if m["resto"].strip():
                secciones[actual].append(m["resto"].strip())
            continue

        if actual and linea.strip():
            secciones[actual].append(linea.strip())

    if not numero:
        raise NotaInvalida("No se encuentra el número de albarán.")

    nota = Nota(
        numero=numero,
        cliente=cliente,
        fecha=fecha,
        hora=hora,
        vehiculo=vehiculo,
        repuestos=" ".join(secciones["repuestos"]),
        trabajos=" ".join(secciones["trabajos"]),
        recomendaciones=" ".join(secciones["recomendaciones"]),
    )
    if not cliente:
        nota.avisos.append("Falta el cliente.")
    if not nota.trabajos:
        nota.avisos.append("No hay sección de trabajos realizados.")
    return nota
