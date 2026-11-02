# CLAUDE.md

Guía para trabajar en este repositorio. Idioma del proyecto: **español** (código, comentarios, documentación y commits).

## Qué es

Automatiza el paso final del flujo de albaranes de un taller: notas dictadas a Gemini (usuario A) → texto listo para **Aniwin 4.3** (usuario B). Fase 1: preparar datos sin tocar Aniwin. Fase 2 (sin implementar): consultas de solo lectura al `.MDB`.

Antes de cambiar nada, leer:

- `docs/01-hechos-confirmados.md`: lo que sabemos con certeza.
- `docs/02-aspectos-abiertos.md`: dudas y decisiones pendientes. **No inventar respuestas**; si algo depende de una duda abierta, indicarlo y actualizar este documento.
- `docs/03-definicion-funcional.md` y `docs/04-copias-seguridad.md`.

## Reglas que no se saltan

1. **Nunca escribir en la base de datos de Aniwin** (`.MDB`). Aniwin calcula totales, IVA y stock y reparte datos en varias tablas. La Fase 2 es solo lectura (`pyodbc`, modo lectura).
2. **Nunca subir datos reales** de clientes: nombres, direcciones, teléfonos, correos, nº de albarán. Usar `XXXX` y `Nombre cliente`. Esto incluye tests, ejemplos, docs y mensajes de commit.
3. **Nunca subir** `config.ini`, copias de `.mdb`/`.accdb`, logs ni credenciales de Google (ya están en `.gitignore`).
4. Probar siempre sobre una **copia** de la base de datos, nunca sobre el archivo original.
5. **No usar librerías no oficiales** para leer Google Keep (por ejemplo `gkeepapi`). Keep solo tiene API oficial con Workspace; con cuenta personal se usará Tasks, Gmail o Sheets.
6. Las notas que no se puedan interpretar **no se descartan**: van a la carpeta de errores y se registran en el log.

## Hechos técnicos que condicionan el código

- Aniwin 4.3; base de datos `C:\AniwinNET\FERNANDO .MDB` (posible espacio antes de `.MDB`, sin confirmar).
- Access de 64 bits, así que Python de **64 bits**. Entorno de ejecución: Windows.
- Cada línea de descripción de Aniwin admite **90 caracteres** (`max_chars_linea` en la configuración).
- Cabecera de albaranes en la tabla `caalcl`. Que las líneas estén en `caalpr` es solo una hipótesis.
- El formato de la nota completa de Keep **no está confirmado**; `parser.py` asume etiquetas `Repuestos:`, `Trabajos realizados:` y `Recomendaciones:`.

## Estructura

```
src/albaranes/parser.py   Extrae datos de la nota
src/albaranes/wrap.py     Ajusta texto a 90 caracteres
src/albaranes/backup.py   Copias del .MDB (con comprobación de archivo en uso)
src/albaranes/main.py     Ejecución principal (origen provisional: carpeta de .txt)
tests/                    Pruebas con pytest
examples/                 Notas de ejemplo anonimizadas
```

## Comandos

```
pip install -r requirements.txt
python -m pytest -q                      # tests
python -m albaranes.main --dry-run       # simulación, no mueve ni escribe archivos
```

## Estilo

- Python 3.10 o superior; tipado con anotaciones; biblioteca estándar siempre que sea posible.
- Cada función nueva con su test. Los tests no pueden depender de datos reales ni de Access instalado.
- Comentarios y mensajes de log en español, claros para alguien con nivel técnico intermedio: el mantenimiento lo hará una persona que no es desarrolladora de Python.
- Cambios de comportamiento → actualizar `docs/` y, si cierran una duda, moverla de `02-aspectos-abiertos.md` a `01-hechos-confirmados.md`.

## Git

- Commits en español, en imperativo y descriptivos.
- Rama principal: `main`.
