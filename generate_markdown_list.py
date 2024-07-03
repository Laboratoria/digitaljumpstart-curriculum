import os
import sys
import csv
import json
import yaml

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

def save_to_csv(records, filename):
    keys = records[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(records)

def save_to_json(records, filename):
    with open(filename, 'w') as output_file:
        json.dump(records, output_file, indent=2)

def save_to_yaml(records, filename):
    with open(filename, 'w') as output_file:
        yaml.dump(records, output_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_markdown_list.py <root_directory>")
        sys.exit(1)

    root_dir = sys.argv[1]
    records = generate_markdown_list(root_dir)

    save_to_csv(records, 'markdown_files.csv')
    save_to_json(records, 'markdown_files.json')
    save_to_yaml(records, 'markdown_files.yaml')

    print("Files have been saved: markdown_files.csv, markdown_files.json, markdown_files.yaml")
