# Automatización de albaranes (Aniwin)

Herramienta para que el usuario B deje de teclear a mano en **Aniwin 4.3** lo que el usuario A ya ha dictado a Gemini.

> **Estado:** v0.1, definición y esqueleto. El origen de las notas (Keep, Tasks u otro) y el formato de importación de Aniwin **no están cerrados**. Ver [`docs/02-aspectos-abiertos.md`](docs/02-aspectos-abiertos.md).

## Qué hace (Fase 1)

1. Lee las notas nuevas de un origen (ahora, una carpeta de archivos `.txt`; el origen real se decidirá).
2. Extrae nº de albarán, cliente, fecha y las secciones de repuestos, trabajos realizados y recomendaciones.
3. Divide los textos en líneas de 90 caracteres como máximo, sin cortar palabras.
4. Genera un texto listo para pegar en Aniwin (o, más adelante, un archivo de importación).
5. Registra en un log lo procesado y los errores.

**No escribe en la base de datos de Aniwin.** La Fase 2 (solo lectura del `.MDB`) está descrita pero sin implementar.

## Estructura

```
config.example.ini        Configuración de ejemplo (copiar a config.ini)
docs/                     Hechos confirmados, dudas, definición funcional, copias de seguridad
examples/                 Notas de ejemplo ANONIMIZADAS
src/albaranes/            Código (parser, ajuste a 90 caracteres, copias, ejecución)
tests/                    Pruebas
```

## Instalación en Windows

1. Instalar Python 3.12 o superior, **64 bits**, marcando *Add Python to PATH* (Access es de 64 bits).
2. En la carpeta del proyecto: `python -m venv .venv`, luego `.venv\Scripts\activate` y `pip install -r requirements.txt`.
3. Copiar `config.example.ini` a `config.ini` y ajustar las rutas.
4. Probar: `python -m albaranes.main --dry-run`.
5. Programar con el Programador de tareas de Windows (al iniciar sesión y cada pocos minutos).

## Reglas del proyecto

- **Nunca** subir datos reales de clientes (nombres, direcciones, teléfonos, correos, nº de albarán reales). Usar `XXXX` y `Nombre cliente`.
- **Nunca** subir `config.ini`, copias del `.MDB` ni logs (están en `.gitignore`).
- Probar siempre sobre una **copia** de la base de datos.
