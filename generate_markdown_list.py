import os
import yaml
import json
import pandas as pd

repo_path = '.'

markdown_files = []

for root, dirs, files in os.walk(repo_path):
    for file in files:
        if file.endswith('.md'):
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, repo_path)
            
            # Leer el contenido del archivo y extraer el header1
            with open(full_path, 'r', encoding='utf-8') as md_file:
                for line in md_file:
                    if line.startswith('# '):
                        header1 = line.strip().lstrip('# ').strip()
                        break
                else:
                    header1 = None  # No se encontró un encabezado de nivel 1

            markdown_files.append({'Path': relative_path, 'Header1': header1})

# Guardar en YAML
with open('markdown_files.yaml', 'w') as yaml_file:
    yaml.dump(markdown_files, yaml_file, default_flow_style=False, allow_unicode=True)

# Guardar en JSON
with open('markdown_files.json', 'w') as json_file:
    json.dump(markdown_files, json_file, indent=4, ensure_ascii=False)

# Guardar en CSV
df = pd.DataFrame(markdown_files)
df.to_csv('markdown_files.csv', index=False)
