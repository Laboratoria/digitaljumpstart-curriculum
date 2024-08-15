# Currícula prototipo
Este repositorio contiene una estructura fija (inflexible) de carpetas para "programs", "skills", "modules", "activities" y "topics". Todo es MD excepto un archivo de "metadatos" para cada activity en formato JSON.

Asímismo, contiene scripts para procesar los archivos, extrayendo y limpiando información relevante para generar listados en formatos CSV y JSON. Además, sincroniza estos datos con una base de datos en PostgreSQL a través de un endpoint de API REST. Esos datos se consimirán en el front-end.

## Descripción General del script Python
Se ejecuta como GH actions
El script generate_markdown_list.py automatiza el procesamiento de archivos de currícula y su sincronización con una base de datos centralizada. Las principales funcionalidades del script incluyen:

### Procesamiento de Archivos Markdown y JSON:
- Limpieza y validación de archivos de configuración JSON (escapes y e mojis).
- Extracción de información relevante de cada archivo Markdown.
- Generación de listados en formatos CSV y JSON.
- Sincronización con Base de Datos.

- etc.
- etc.
