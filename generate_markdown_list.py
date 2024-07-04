
import os
import json
import csv
import yaml
import logging

# Configuración del logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_markdown_list(root_dir):
    markdown_list = []
    keys = set()
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md") or file.endswith("_CONFIG.json"):
                file_path = os.path.join(subdir, file)
                track, skill, module = get_levels(file_path, root_dir)
                title = get_header(file_path) if file.endswith(".md") else file
                file_type = get_file_type(file_path)
                
                if file_type == "config":
                    additional_info = get_config_content(file_path)
                else:
                    additional_info = {}

                markdown_entry = {
                    "track": track,
                    "skill": skill,
                    "module": module,
                    "title": title,
                    "path": file_path[2:],  # Remove the leading "./"
                    "type": file_type,
                    **additional_info
                }
                keys.update(markdown_entry.keys())
                logging.debug(f"Appending entry: {markdown_entry}")  # Debugging output
                markdown_list.append(markdown_entry)
    
    # Asegurar que todos los diccionarios tengan las mismas llaves
    for entry in markdown_list:
        for key in keys:
            if key not in entry:
                entry[key] = None

    return markdown_list

def get_header(file_path):
    if file_path.endswith(".md"):
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith("# "):
                    return line[2:].strip()
    return None

def get_levels(file_path, root_dir):
    parts = os.path.relpath(file_path, root_dir).split(os.sep)
    if parts[-1].endswith(".md") or parts[-1].endswith("_CONFIG.json"):
        parts = parts[:-1]
    track = parts[0] if len(parts) > 0 else None
    skill = parts[1] if len(parts) > 1 else None
    module = parts[2] if len(parts) > 2 else None
    return track, skill, module

def get_file_type(file_path):
    if file_path.endswith("_CONFIG.json"):
        return "config"
    if "activities" in file_path and file_path.endswith(".md") and not file_path.endswith("README.md"):
        return "activity"
    if file_path.endswith("README.md"):
        return "container"
    return "container"

def get_config_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            logging.debug(f"Config content for {file_path}: {config}")  # Debugging output
            return config
    except json.JSONDecodeError as e:
        logging.error(f"Error reading JSON from {file_path}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error reading {file_path}: {e}")
    return {}

def save_to_csv(data, filename):
    if not data:
        logging.warning(f"No data to write to {filename}")
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    logging.info(f"Data saved to {filename}")

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    logging.info(f"Data saved to {filename}")

def save_to_yaml(data, filename):
    with open(filename, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
    logging.info(f"Data saved to {filename}")

if __name__ == "__main__":
    root_dir = "."  # Asegúrate de estar en la raíz del repositorio
    markdown_list = generate_markdown_list(root_dir)

    save_to_csv(markdown_list, "markdown_files.csv")
    save_to_json(markdown_list, "markdown_files.json")
    save_to_yaml(markdown_list, "markdown_files.yaml")


"""
import os
import json
import csv
import yaml

def generate_markdown_list(root_dir):
    markdown_list = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(subdir, file)
                track, skill, module = get_levels(file_path, root_dir)
                title = get_header(file_path)
                file_type = get_file_type(file_path)
                markdown_list.append({
                    "track": track,
                    "skill": skill,
                    "module": module,
                    "title": title,
                    "path": file_path,
                    "type": file_type
                })
    return markdown_list

def get_header(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("# "):
                return line[2:].strip()
    return None

def get_levels(file_path, root_dir):
    parts = os.path.relpath(file_path, root_dir).split(os.sep)
    # Excluir el archivo del conteo, considerar solo carpetas
    if parts[-1].endswith(".md"):
        parts = parts[:-1]
    track = parts[0] if len(parts) > 0 else None
    skill = parts[1] if len(parts) > 1 else None
    module = parts[2] if len(parts) > 2 else None
    return track, skill, module

def get_file_type(file_path):
    parts = file_path.split(os.sep)
    if "activity" in parts:
        return "activity"
    elif "topics" in parts:
        return "topic"
    elif file_path.endswith("README.md"):
        return "container"
    elif file_path.endswith("CONFIG.md"):
        return "config"
    else:
        return "container"

def save_to_csv(data, filename):
    if not data:
        print(f"No data to write to {filename}")
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def save_to_yaml(data, filename):
    with open(filename, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

if __name__ == "__main__":
    root_dir = "."  # Asegúrate de estar en la raíz del repositorio
    markdown_list = generate_markdown_list(root_dir)

    save_to_csv(markdown_list, "markdown_files.csv")
    save_to_json(markdown_list, "markdown_files.json")
    save_to_yaml(markdown_list, "markdown_files.yaml")
"""
