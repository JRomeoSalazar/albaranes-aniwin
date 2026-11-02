# Hechos confirmados

Procede de las capturas y respuestas del usuario B. Los datos personales de las capturas **no se reproducen** aquí.

## Flujo actual

1. El usuario A dicta una nota de voz a Google Gemini con el nº de albarán y los trabajos realizados.
2. Gemini crea una nota en Google Keep.
3. El usuario B lee la nota y actualiza el albarán en Aniwin.

## Sistemas y equipo

| Elemento | Dato |
| --- | --- |
| Programa de gestión | Aniwin 4.3 |
| Base de datos | Archivo Access `C:\AniwinNET\FERNANDO .MDB` |
| Access | 64 bits |
| Python | No instalado en el equipo |
| Equipo | Se enciende y apaga a diario; se puede dejar encendido por la noche |
| Importación en Aniwin | Existe la posibilidad; formato sin confirmar |

## Nota de Keep creada por Gemini (lo visto en captura)

```
Albarán XXXX - Nombre cliente
Fecha: DD/MM/AAAA | Hora: HH:MM | Albarán Nº: XXXX
Cliente: Nombre cliente
Vehículo: <descripción breve>
```

El usuario B afirma que los trabajos se ordenan en secciones de **repuestos, trabajos realizados y recomendaciones**, en líneas de **90 caracteres** (lo que admite cada línea de Aniwin). **No hemos visto aún una nota completa.**

## Albarán en Aniwin

- Pantalla "Albarán Cliente": serie y nº, cliente (por código), fecha, hora y estado (`Pendiente`, `Facturado`).
- Cuadrícula de líneas con: código, descripción, cantidad, precio, % descuento, % IVA, total, observaciones.
- Cliente y artículo se eligen desde una tabla de selección del programa.
- Ejemplo de líneas reales: artículos con código, y una línea de mano de obra `MOTUB` ("tubelizar rueda").
- Albarán impreso: concepto `MO`, descripción multilínea ("TRABAJOS REALIZADOS. MANO DE OBRA", informe técnico, recomendaciones), cantidad 1,00, IVA 21 %.

## Base de datos (capturas de Access)

- Tabla `caalcl`: cabecera de albaranes. Campos vistos: `cal_serie`, `cal_nro`, `cal_fecha`, `cal_cliente`, `cal_rsocial`, `cal_direc`, `cal_pobla`, `cal_provin`, `cal_cif`, `cal_ctacli`, `cal_tipo`, `cal_cpos`, `cal_fpago`, `cal_impbru`, `cal_dtogen`, `cal_dtopp`, `cal_tdtospp`, `cal_tdtosgen`, `cal_tdtos`, `cal_total`, `cal_repre`, `cal_bultos`, `cal_kilos`, `cal_portes`, `cal_marca`, `cal_acuenta`, `cal_tipocomi`, `cal_ref`, `cal_coment1`.
- Tablas que aparecen en el panel de Access: `caalcl`, `caalpr`, `caarpr`, `cabamo`, `bajasbo`, `BANCOS`, `CABASI`, entre otras.
- Hipótesis (**sin confirmar**): las líneas del albarán están en `caalpr`.

## Decisiones tomadas

- No escribir directamente en las tablas de Aniwin: calcula totales, IVA y stock, y guarda datos repartidos en varias tablas.
- Python de 64 bits (coincide con Access de 64 bits).
- Copias de seguridad periódicas del `.MDB` (ver [`04-copias-seguridad.md`](04-copias-seguridad.md)).
- Fase 1 sin tocar Aniwin; Fase 2 solo con lectura.
