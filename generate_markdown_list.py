import os
import json
import csv
import yaml

def generate_markdown_list(root_dir):
    markdown_list = []
    config_data = {}
    
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(subdir, file)
                rel_file_path = os.path.relpath(file_path, root_dir)
                track, skill, module = get_levels(rel_file_path)
                title = get_header(file_path)
                file_type = get_file_type(file_path)
                difficulty, learning, time, discord_URL_ES, discord_URL_PT = (None, None, None, None, None)
                
                if "activity" in file_path:
                    base_name = file.rsplit("_", 1)[0]
                    config_file = os.path.join(subdir, f"{base_name}_CONFIG.md")
                    if config_file not in config_data:
                        config_data[config_file] = parse_config_file(config_file)
                    config_values = config_data.get(config_file, {})
                    difficulty = config_values.get("difficulty")
                    learning = config_values.get("learning")
                    time = config_values.get("time")
                    discord_URL_ES = config_values.get("discord_URL_ES")
                    discord_URL_PT = config_values.get("discord_URL_PT")
                
                markdown_list.append({
                    "track": track,
                    "skill": skill,
                    "module": module,
                    "title": title,
                    "path": rel_file_path,
                    "type": file_type,
                    "difficulty": difficulty,
                    "learning": learning,
                    "time": time,
                    "discord_URL_ES": discord_URL_ES,
                    "discord_URL_PT": discord_URL_PT
                })
    return markdown_list

def get_header(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("# "):
                return line[2:].strip()
    return None

def get_levels(file_path):
    parts = file_path.split(os.sep)
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

def parse_config_file(file_path):
    config = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith("# "):
                    break
                if ":" in line:
                    key, value = line.split(":", 1)
                    config[key.strip()] = value.strip()
    return config

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
