# Definición funcional (v0.1)

## Objetivo

Que el usuario B no teclee a mano el contenido que el usuario A ya dictó: un script lee la nota, la ordena y deja los datos listos para Aniwin.

## Alcance

**Incluye:** leer notas nuevas, extraer datos, ajustar a 90 caracteres por línea, preparar la salida, registrar resultados y hacer copias de seguridad.

**No incluye (por ahora):** escribir en tablas internas de Aniwin, cambiar la forma de trabajar del usuario A (salvo fijar el formato de la nota), facturación o stock.

## Fases

**Fase 1: preparar los datos (sin tocar Aniwin).** Detectar notas, extraer, ajustar, generar salida, registrar. El usuario B revisa e importa o pega.

**Fase 2: ayudas de solo lectura.** Buscar código de cliente y de artículo, comprobar que el albarán existe y no está facturado, derivar a revisión los casos ambiguos. Solo si la Fase 1 funciona y se confirma la estructura de tablas.

## Requisitos

| ID | Requisito | Fase | Módulo |
| --- | --- | --- | --- |
| RF-01 | Detectar notas nuevas y no procesar dos veces la misma. | 1 | `main.py` |
| RF-02 | Extraer nº de albarán, cliente, fecha y hora. | 1 | `parser.py` |
| RF-03 | Separar repuestos, trabajos realizados y recomendaciones. | 1 | `parser.py` |
| RF-04 | Líneas de 90 caracteres como máximo, sin cortar palabras. | 1 | `wrap.py` |
| RF-05 | Generar salida para Aniwin (texto para pegar; luego importación). | 1 | `main.py` |
| RF-06 | Marcar cada nota como pendiente, procesada o con error. | 1 | `main.py` |
| RF-07 | Registro con fecha, nota y resultado. | 1 | `main.py` |
| RF-08 | Avisar de notas con error. | 1 | `main.py` |
| RF-09 | Ajustes en `config.ini`. | 1 | `main.py` |
| RF-10 | Copia de la base de datos antes de cada importación. | 1 | `backup.py` |
| RF-11 a RF-14 | Búsqueda de cliente y artículos, comprobación de albarán y revisión de ambiguos, en solo lectura. | 2 | Pendiente |

## Restricciones y riesgos

| Riesgo | Mitigación |
| --- | --- |
| Keep solo tiene API oficial con Workspace. | Confirmar tipo de cuenta; si es personal, usar Tasks, Gmail o Sheets. No usar librerías no oficiales. |
| Escribir en el `.MDB` puede dejar albaranes descuadrados. | No escribir; importación de Aniwin y copias. |
| Cliente anotado por nombre y no por código. | Revisión del usuario B; en Fase 2, aviso si hay varias coincidencias. |
| Gemini cambia el formato de la nota. | Instrucción fija; notas no reconocidas a revisión. |
| Equipo apagado. | El script procesa lo pendiente al arrancar. |
| Python y driver de Access de distinta arquitectura. | Python de 64 bits. |
