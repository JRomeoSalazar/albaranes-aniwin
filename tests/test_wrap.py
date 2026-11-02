from albaranes.wrap import ajustar


def test_lineas_no_superan_90():
    texto = "palabra " * 60
    assert all(len(l) <= 90 for l in ajustar(texto))


def test_no_corta_palabras():
    lineas = ajustar("a" * 85 + " bbbbbbbbbb")
    assert lineas == ["a" * 85, "bbbbbbbbbb"]


def test_palabra_mas_larga_que_el_ancho_se_divide():
    assert all(len(l) <= 90 for l in ajustar("x" * 200))


def test_conserva_lineas_vacias():
    assert ajustar("uno\n\ndos") == ["uno", "", "dos"]
