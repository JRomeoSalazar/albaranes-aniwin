from datetime import datetime

import pytest

from albaranes.backup import ArchivoEnUso, depurar, hacer_copia


def test_copia_con_fecha_en_el_nombre(tmp_path):
    mdb = tmp_path / "BASE .MDB"
    mdb.write_bytes(b"datos")
    copia = hacer_copia(mdb, tmp_path / "copias", datetime(2026, 11, 2, 18, 30))
    assert copia.name == "BASE_2026-11-02_1830.mdb"
    assert copia.read_bytes() == b"datos"
    assert mdb.read_bytes() == b"datos"


def test_no_copia_si_esta_en_uso(tmp_path):
    mdb = tmp_path / "BASE.mdb"
    mdb.write_bytes(b"x")
    (tmp_path / "BASE.ldb").write_bytes(b"")
    with pytest.raises(ArchivoEnUso):
        hacer_copia(mdb, tmp_path / "copias")


def test_depurar_conserva_diarias_y_una_por_mes(tmp_path):
    for dia in range(1, 6):
        (tmp_path / f"BASE_2026-10-{dia:02d}_1800.mdb").write_bytes(b"x")
    (tmp_path / "BASE_2026-09-15_1800.mdb").write_bytes(b"x")
    eliminadas = depurar(tmp_path, diarias=2, mensuales=12)
    nombres = {c.name for c in eliminadas}
    # Se conservan las 2 más recientes, la más antigua de octubre y la de septiembre.
    assert nombres == {"BASE_2026-10-02_1800.mdb", "BASE_2026-10-03_1800.mdb"}
