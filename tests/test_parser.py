from pathlib import Path

import pytest

from albaranes.parser import NotaInvalida, interpretar

EJEMPLO = Path(__file__).parent.parent / "examples" / "nota_ejemplo.txt"


def test_nota_de_ejemplo():
    n = interpretar(EJEMPLO.read_text(encoding="utf-8"))
    assert n.numero == "XXXX"
    assert n.cliente == "Nombre cliente"
    assert n.fecha == "29/09/2026"
    assert n.hora == "09:30"
    assert "Bicicleta eléctrica" in n.vehiculo
    assert n.repuestos.startswith("Cubierta")
    assert n.trabajos.startswith("Cambio de cubierta")
    assert n.recomendaciones.startswith("Revisar la presión")
    assert n.avisos == []


def test_sin_numero_es_invalida():
    with pytest.raises(NotaInvalida):
        interpretar("Cliente: Alguien\nTrabajos realizados:\nAlgo")


def test_sin_trabajos_genera_aviso():
    n = interpretar("Albarán 1 - Cliente de prueba\n")
    assert "No hay sección de trabajos realizados." in n.avisos
