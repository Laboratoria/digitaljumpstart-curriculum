# Reto 1.1: Fundamentos del modelo RFM

**Dificultad:** 🌻 

**Aprendizaje:** 🍯🍯 

**Tiempo:** ⏱️️⏱️️⏱️️⏱️️ 3-5 hrs.


---


## Meta de Aprendizaje

Aprenderás a identificar en un conjunto de datos las variables necesarias para el análisis de clientes mediante el método RFM. Para lograrlo, primero profundizarás en el concepto de esta técnica de segmentación y deberás unir dos tablas de datos con una fórmula. Con esto, estarás preparada para aplicar la técnica de forma efectiva en los siguientes retos.

## Descripción

Revisa los contenidos disponibles en los materiales proporcionados, así como la base de datos, y asegúrate de que eres capaz de responde a las siguientes preguntas antes de unir las tablas y generar columnas para las variables RFM:

1. ¿Qué es RFM?
2. ¿Cuáles variables tengo en mi base de datos para realizar este análisis?
3. ¿Cuál variable o conjunto de variables corresponde a Recencia, cuál a Frecuencia y cuál a Monto?
4. ¿Puedo utilizar alguna fórmula para combinar variables y obtener una única columna para Frecuencia y otra para Monto?
5. ¿Cómo "traigo" los datos de la base de datos de transacciones para la base de datos principal y poder así usar alguna fórmula para calcular la Recencia?


### Cumples con la meta de aprendizaje si:

- [x] Logras responder para ti misma a todas las preguntas planteadas en la descripción.
- [x] Logras unir las dos bases de datos a través de una fórmula.
- [x] Logras obtener una columna que represente la Recencia, una para Frecuencia y otra para Monto.


## Insumos para tu aprendizaje
<!-- Los enlaces a topics, hay que ponerlos usando este patrón  ?lang=ES&track=DAT&skill=03_segmentation&module=01_rfmrfm_prompt_ES.md-->
<!-- luego será compeltado por el script en python del repo en GH -->
- [📄 Texto: Base de Datos 1 y descripción de Variables](https://docs.google.com/spreadsheets/d/1nE1yZuE-bzZ2Ot4xjbq3zADqTcNXnNA4_ksE7uYE2JI/copy?).
- [📄 Texto: Base de Datos 2 con la fecha de la ultima compra del cliente](https://docs.google.com/spreadsheets/d/1lM0f0Pu78rq4t-eHCHnPo0T8lIS0F4bs22WS4gtCQWk/copy?).
- [📄 Texto:  Concepto segmentación de clientes](https://docs.google.com/document/d/1I3_bay1ymFa0iMRz6W_C_mpmnahMdMs5_0UEiKf1jTo/edit?usp=sharing).
- [📺 Video: Podcast segmentación de clientes](https://open.spotify.com/episode/23JZkyLP28b2U9E9LIEaWV).
- [📄 Texto: Unir tablas en Google Sheets](https://docs.google.com/document/d/1mPYh7wmMmqUl5k8lACskw7Jav315NVZHrNymf6NwJss/edit?usp=sharing).
- [📄 Texto: Documentación VLOOKUP](https://support.google.com/docs/answer/3093318?hl=es).
- [📄 Video: El uso de las fórmulas INDEX + MATCH](https://www.youtube.com/watch?v=QzCVTurf5vs).
- [🤖 🤝 Texto: Usando IA para entender mejor RFM](?lang=ES&track=DAT&skill=03_segmentation&module=01_rfmrfm_prompt_ES.md)


## Pauta de Trabajo

- Crea una copia del archivo en el que trabajaste en los retos anteriores y agrega una hoja (sheet) con el nombre de este reto. Recuerda que en este reto tenemos dos archivos con los datos necesarios para realizar el análisis. Puedes probar la fórmula [IMPORTRANGE](https://www.loom.com/share/80681eee41704fd1a919a8fabde781ac?sid=9fc7ea93-1ef5-4fa5-b691-3bed2e363b1d) para traer los datos de un archivo a otro, o simplemente copiar y pegar los datos.
- Lee las descripciones de las variables que se encuentran en el archivo de la base de datos.
- Revisa el concepto de RFM y asegúrate de comprender qué significa Recencia, Frecuencia y Monto.
- Identifica las variables que puedes utilizar para segmentar los clientes por Recencia, Frecuencia y Monto.
- Utiliza las fórmulas VLOOKUP o INDEX+MATCH para traer la fecha de la última compra de acuerdo con el id_cliente.
- Calcula lo necesario para obtener una única columna que indique los días transcurridos desde la última compra.
- Suma el Monto y la Frecuencia de compra, tanto en línea como en tienda.
- Tienes libertad para probar y analizar los datos como prefieras.
- **Asegúrate de comprender lo que estás haciendo.** No te limites solo a las preguntas planteadas; **explora, analiza, prueba**, y busca nuevas formas de abordar el problema.

Aquí tienes algunos resultados de referencia para asegurarte de que vas por buen camino con tu análisis.

![image](https://raw.githubusercontent.com/Laboratoria/digitaljumpstart-curriculum/main/DAT/00_assets/image_solucion_rfm.png)

Tip: Utiliza la fórmula DATE y la fecha del último día del año de 2023 para calcular la Recencia.

---

¡Diviértete y disfruta del proceso de aprendizaje! Recuerda que sentirte confundida o desorientada es parte natural del proceso.

