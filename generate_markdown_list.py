import os

def get_first_h2_from_markdown(md_content):
    lines = md_content.split('\n')
    for line in lines:
        if line.startswith('## '):
            return line[3:]
    return ''

def get_first_h1_from_markdown(md_content):
    lines = md_content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:]
    return ''

def get_config_data(config_content):
    data = {}
    lines = config_content.split('\n')
    for line in lines:
        if line.startswith('difficulty:'):
            data['difficulty'] = line.split('difficulty:')[1].strip()
        elif line.startswith('learning:'):
            data['learning'] = line.split('learning:')[1].strip()
        elif line.startswith('time:'):
            data['time'] = line.split('time:')[1].strip()
        elif line.startswith('discord_URL_ES:'):
            data['discord_URL_ES'] = line.split('discord_URL_ES:')[1].strip()
    return data

def generate_markdown_list(root_dir):
    records = []

    for track_name in os.listdir(root_dir):
        track_path = os.path.join(root_dir, track_name)
        if os.path.isdir(track_path):
            for skill_name in os.listdir(track_path):
                skill_path = os.path.join(track_path, skill_name)
                if os.path.isdir(skill_path):
                    for module_name in os.listdir(skill_path):
                        module_path = os.path.join(skill_path, module_name)
                        if os.path.isdir(module_path):
                            # Process README.md
                            readme_path = os.path.join(module_path, 'README.md')
                            if os.path.isfile(readme_path):
                                with open(readme_path, 'r') as file:
                                    content = file.read()
                                title = get_first_h2_from_markdown(content)
                                record = {
                                    "track": track_name,
                                    "skill": skill_name,
                                    "module": module_name,
                                    "type": "container",
                                    "title": title,
                                    "path_md": readme_path
                                }
                                records.append(record)

                            # Process activities
                            activity_path = os.path.join(module_path, 'activity')
                            if os.path.isdir(activity_path):
                                for activity_file in os.listdir(activity_path):
                                    if activity_file.endswith('_ES.md'):
                                        es_path = os.path.join(activity_path, activity_file)
                                        config_path = es_path.replace('_ES.md', '_CONFIG.md')
                                        if os.path.isfile(config_path):
                                            with open(es_path, 'r') as es_file:
                                                es_content = es_file.read()
                                            with open(config_path, 'r') as config_file:
                                                config_content = config_file.read()

                                            title = get_first_h1_from_markdown(es_content)
                                            config_data = get_config_data(config_content)

                                            record = {
                                                "track": track_name,
                                                "skill": skill_name,
                                                "module": module_name,
                                                "type": "activity",
                                                "title": title,
                                                "path_md": es_path
                                            }
                                            record.update(config_data)
                                            records.append(record)
    return records

root_dir = 'path_to_your_directory'
records = generate_markdown_list(root_dir)

# Now you can print or save `records` as needed
import json
print(json.dumps(records, indent=2))


"""
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
"""
