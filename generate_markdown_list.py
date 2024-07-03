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
                track, skill, module, file_type = get_levels_and_type(file_path, root_dir)
                title = get_header(file_path)
                markdown_list.append({
                    "track": track,
                    "skill": skill,
                    "module": module,
                    "type": file_type,
                    "title": title,
                    "path": file_path
                })
    return markdown_list

def get_header(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("# "):
                return line[2:].strip()
    return None

def get_levels_and_type(file_path, root_dir):
    parts = os.path.relpath(file_path, root_dir).split(os.sep)
    # Excluir el archivo del conteo, considerar solo carpetas
    if parts[-1].endswith(".md"):
        parts = parts[:-1]
    track = parts[0] if len(parts) > 0 else None
    skill = parts[1] if len(parts) > 1 else None
    module = parts[2] if len(parts) > 2 else None

    # Determinar el tipo
    file_type = "container"
    if "activities" in parts:
        file_type = "activity"
    elif "topics" in parts:
        file_type = "topic"

    return track, skill, module, file_type

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
