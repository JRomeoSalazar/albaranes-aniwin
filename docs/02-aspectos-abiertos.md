# Aspectos abiertos

## A. Dudas que bloquean el diseño

| # | Duda | Por qué importa | Responde |
| --- | --- | --- | --- |
| 1 | ¿La cuenta de Google es personal o Workspace? | Keep solo tiene API oficial con Workspace. | Usuario A o B |
| 2 | ¿Gemini puede enviar la nota a Google Tasks u otro destino con API en lugar de a Keep? | Es la alternativa oficial con cuenta personal. | Usuario A |
| 3 | ¿Cómo es una nota de Keep completa (repuestos, trabajos, recomendaciones)? | Define las etiquetas que reconoce el parser. | Usuario A |
| 4 | ¿Qué formato de importación admite Aniwin 4.3? | Decide entre archivo importable o texto para pegar. | Usuario B / proveedor |

## B. Otras dudas

5. ¿La importación crea albaranes nuevos o actualiza uno existente? ¿El albarán ya existe cuando llega la nota?
6. ¿Cómo se relaciona el nº dictado con la serie y el nº de Aniwin? ¿La serie es siempre A6?
7. ¿El cliente se identifica solo por nombre? ¿Puede haber nombres repetidos?
8. ¿Los repuestos se dictan por nombre? ¿Quién fija códigos y precios (`MO`, `MOTUB`)?
9. ¿Las líneas están en `caalpr`? Confirmarlo con el proveedor de Aniwin.
10. ¿Nombre exacto del archivo (¿espacio antes de `.MDB`?) y cuántos usuarios lo usan a la vez?
11. ¿Existen copias de seguridad hoy? ¿Dónde se guardarán las nuevas?
12. ¿En qué equipo se instala Python, con qué permisos?
13. ¿Existe una empresa o copia de pruebas en Aniwin?
14. ¿Qué se hace con las notas procesadas y con las que dan error?

## C. Ideas con base parcial (no cerradas)

| Aspecto | Idea actual | Qué falta para cerrarla |
| --- | --- | --- |
| Origen de datos | Abstraer el origen (`carpeta`, `tasks`, `gmail`, `sheets`) para cambiarlo sin tocar el resto. Desarrollo con carpeta de `.txt`. | Respuestas 1 y 2. |
| Formato de nota | El parser busca etiquetas `Repuestos:`, `Trabajos realizados:`, `Recomendaciones:` y la línea `Fecha: ... \| Hora: ... \| Albarán Nº: ...`. | Una nota completa real. |
| Si el origen es Tasks/Gmail | Instrucción fija en Gemini para forzar el formato de etiquetas. | Respuesta 2. |
| Salida | Texto listo para pegar en la descripción de Aniwin, líneas de 90 caracteres. Después, archivo de importación. | Respuesta 4. |
| Fase 2 | Con `pyodbc`, solo lectura, buscar código de cliente y artículos, y comprobar que el albarán no está `Facturado`. | Respuestas 7, 8 y 9. |
| Copias | Diaria + una antes de cada importación; 30 diarias y 12 mensuales; segunda ubicación fuera del equipo. | Respuesta 11. |
| Notas con error | Mover a carpeta de errores y avisar; nunca descartar. | Respuesta 14. |
| Programación | Programador de tareas de Windows, al iniciar sesión y cada pocos minutos. | Respuesta 12. |
