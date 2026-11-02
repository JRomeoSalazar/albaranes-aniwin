# Copias de seguridad de la base de datos de Aniwin

Se hacen copias periódicas para poder recuperar la base de datos si se produce cualquier error. Las cifras son una **propuesta** por validar con el usuario B.

| Aspecto | Propuesta |
| --- | --- |
| Qué se copia | `C:\AniwinNET\FERNANDO .MDB` (confirmar si Aniwin necesita más archivos). |
| Cuándo | Una copia diaria automática y una extra antes de cada importación. |
| Dónde | Carpeta distinta de la de Aniwin, con fecha y hora en el nombre (`FERNANDO_AAAA-MM-DD_HHMM.mdb`), y una segunda ubicación fuera del equipo (disco externo o nube). |
| Retención | Últimas 30 diarias y una por mes (12 meses). |
| Archivo en uso | Si existe `.ldb`/`.laccdb`, Aniwin está en uso: se reintenta más tarde. |
| Verificación | Comprobar que la copia existe y que su tamaño coincide con el original. Antes de poner en marcha, hacer una prueba real de restauración. |
| Pruebas | Siempre sobre una copia, nunca sobre el archivo original. |

Implementado en `src/albaranes/backup.py`.

## Cómo recuperar

1. Cerrar Aniwin en todos los equipos.
2. Renombrar el archivo actual (no borrarlo).
3. Copiar la copia elegida a la misma carpeta con el nombre original.
4. Abrir Aniwin y revisar los últimos albaranes.
5. Repetir las notas posteriores a la copia; el log indica cuáles son.
