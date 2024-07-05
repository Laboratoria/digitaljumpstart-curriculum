import os
import json
import csv
import yaml
import logging

# Configuración del logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_markdown_list(root_dir):
    markdown_list = []
    keys = [
        "track", "skill", "module", "title", "type", "lang", "sequence",
        "learning", "difficulty", "time", "path", "discord_URL"
    ]
    config_data = {}

    # Cargar archivos de configuración
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith("_CONFIG.json") and "activities" in subdir:
                file_path = os.path.join(subdir, file)
                config_prefix = os.path.splitext(file_path)[0].rsplit('_', 1)[0]
                config_data[config_prefix] = get_config_content(file_path)

    # Cargar archivos markdown
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(subdir, file)
                track, skill, module = get_levels(file_path, root_dir)
                file_type = get_file_type(file_path, subdir, file)
                config_prefix = os.path.splitext(file_path)[0].rsplit('_', 1)[0]
                additional_info = config_data.get(config_prefix, {})

                lang = get_lang(file)
                sequence = get_sequence(subdir, file)
                title = get_title(file_path, file_type)

                if file_type == "container":
                    titles = get_container_titles(file_path)
                    for i, t in enumerate(titles):
                        lang_key = "ES" if i == 0 else "PT"
                        markdown_list.append(create_entry(
                            track, skill, module, t, file_type, lang_key, sequence, additional_info, file_path[2:]
                        ))
                else:
                    markdown_list.append(create_entry(
                        track, skill, module, title, file_type, lang, sequence, additional_info, file_path[2:]
                    ))

    # Asegurar llaves consistentes
    for entry in markdown_list:
        for key in keys:
            if key not in entry:
                entry[key] = None

    return markdown_list

def create_entry(track, skill, module, title, file_type, lang, sequence, additional_info, path):
    return {
        "track": track,
        "skill": skill,
        "module": module,
        "title": title,
        "type": file_type,
        "lang": lang,
        "sequence": sequence,
        "learning": additional_info.get("learning"),
        "difficulty": additional_info.get("difficulty"),
        "time": additional_info.get("time"),
        "path": path,
        "discord_URL": additional_info.get("discord_URL") if lang == "ES" else additional_info.get("discord_URL_PT")
    }

def get_title(file_path, file_type):
    if file_type in ["activity", "topic"]:
        return get_header(file_path)
    return None

def get_lang(file):
    if file.endswith("_ES.md"):
        return "ES"
    elif file.endswith("_PT.md"):
        return "PT"
    return None

def get_sequence(subdir, file):
    if "activities" in subdir:
        return file[:2]
    return None

def get_header(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("# "):
                return line[2:].strip()
    return None

def get_container_titles(file_path):
    titles = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("## "):
                titles.append(line[3:].strip())
                if len(titles) == 2:
                    break
    return titles

def get_levels(file_path, root_dir):
    parts = os.path.relpath(file_path, root_dir).split(os.sep)
    if parts[-1].endswith((".md", "_CONFIG.json")):
        parts = parts[:-1]
    return (parts[0] if len(parts) > 0 else None,
            parts[1] if len(parts) > 1 else None,
            parts[2] if len(parts) > 2 else None)

def get_file_type(file_path, subdir, file):
    if file.endswith("_CONFIG.json"):
        return "config"
    if "activities" in subdir and file.endswith(".md") and not file.endswith("README.md"):
        return "activity"
    if "topics" in subdir and file.endswith(".md") and not file.endswith("README.md"):
        return "topic"
    if file.endswith("README.md"):
        return "container"
    return "container"

def get_config_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            logging.debug(f"Config content for {file_path}: {config}")
            return {
                "difficulty": config.get("difficulty"),
                "learning": config.get("learning"),
                "time": config.get("time"),
                "discord_URL": config.get("discord_URL", {}).get("ES"),
                "discord_URL_PT": config.get("discord_URL", {}).get("PT")
            }
    except (json.JSONDecodeError, Exception) as e:
        logging.error(f"Error reading JSON from {file_path}: {e}")
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
    root_dir = "."
    markdown_list = generate_markdown_list(root_dir)

    save_to_csv(markdown_list, "markdown_files.csv")
    save_to_json(markdown_list, "markdown_files.json")
    save_to_yaml(markdown_list, "markdown_files.yaml")



"""
import os
import json
import csv
import yaml
import logging

# Configuración del logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_markdown_list(root_dir):
    markdown_list = []
    keys = [
        "track", "skill", "module", "title", "type", "lang", "sequence",
        "learning", "difficulty", "time", "path", "discord_URL"
    ]
    config_data = {}  # Para almacenar temporalmente los datos del archivo de configuración

    # Primero recorrer para cargar los archivos de configuración
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith("_CONFIG.json") and "activities" in subdir:
                file_path = os.path.join(subdir, file)
                additional_info = get_config_content(file_path)
                config_prefix = os.path.splitext(file_path)[0].rsplit('_', 1)[0]
                config_data[config_prefix] = additional_info

    # Luego recorrer para cargar los archivos markdown
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(subdir, file)
                track, skill, module = get_levels(file_path, root_dir)
                file_type = get_file_type(file_path)

                config_prefix = os.path.splitext(file_path)[0].rsplit('_', 1)[0]
                additional_info = config_data.get(config_prefix, {
                    "difficulty": None,
                    "learning": None,
                    "time": None,
                    "discord_URL": None
                })

                # Determinar el campo "lang"
                lang = None
                discord_url = None
                if file.endswith("_ES.md"):
                    lang = "ES"
                    discord_url = additional_info.get("discord_URL")
                elif file.endswith("_PT.md"):
                    lang = "PT"
                    discord_url = additional_info.get("discord_URL")

                # Determinar el campo "sequence" para archivos en carpetas "activities"
                sequence = None
                if "activities" in subdir:
                    sequence = file[:2]

                # Obtener el título adecuado
                if file_type in ["activity", "topic"]:
                    title = get_header(file_path)
                elif file_type == "container":
                    titles = get_container_titles(file_path)
                    if titles:
                        if len(titles) > 0:
                            markdown_list.append({
                                "track": track,
                                "skill": skill,
                                "module": module,
                                "title": titles[0],
                                "type": file_type,
                                "lang": "ES",
                                "sequence": sequence,
                                "learning": additional_info.get("learning"),
                                "difficulty": additional_info.get("difficulty"),
                                "time": additional_info.get("time"),
                                "path": file_path[2:],  # Remove the leading "./"
                                "discord_URL": discord_url if lang == "ES" else None
                            })
                        if len(titles) > 1:
                            markdown_list.append({
                                "track": track,
                                "skill": skill,
                                "module": module,
                                "title": titles[1],
                                "type": file_type,
                                "lang": "PT",
                                "sequence": sequence,
                                "learning": additional_info.get("learning"),
                                "difficulty": additional_info.get("difficulty"),
                                "time": additional_info.get("time"),
                                "path": file_path[2:],  # Remove the leading "./"
                                "discord_URL": discord_url if lang == "PT" else None
                            })
                        continue
                    else:
                        title = None
                else:
                    title = None

                markdown_entry = {
                    "track": track,
                    "skill": skill,
                    "module": module,
                    "title": title,
                    "type": file_type,
                    "lang": lang,
                    "sequence": sequence,
                    "learning": additional_info.get("learning"),
                    "difficulty": additional_info.get("difficulty"),
                    "time": additional_info.get("time"),
                    "path": file_path[2:],  # Remove the leading "./"
                    "discord_URL": discord_url
                }
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

def get_container_titles(file_path):
    titles = []
    if file_path.endswith(".md"):
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith("## "):
                    titles.append(line[3:].strip())
                if len(titles) == 2:
                    break
    return titles

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
    if "topics" in file_path and file_path.endswith(".md") and not file_path.endswith("README.md"):
        return "topic"
    if file_path.endswith("README.md"):
        return "container"
    return "container"

def get_config_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            logging.debug(f"Config content for {file_path}: {config}")  # Debugging output
            return {
                "difficulty": config.get("difficulty"),
                "learning": config.get("learning"),
                "time": config.get("time"),
                "discord_URL": config.get("discord_URL", {}).get("ES"),
                "discord_URL_PT": config.get("discord_URL", {}).get("PT")
            }
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
