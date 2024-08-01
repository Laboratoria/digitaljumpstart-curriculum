import os
import json
import re
import csv

def clean_control_characters(json_str):
    # Reemplazar caracteres de escape incorrectos
    json_str = json_str.replace('\\_', '_')
    # Eliminar caracteres de control y manejar caracteres de escape inválidos
    json_str = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', json_str)  # Escapar correctamente las barras invertidas
    return re.sub(r'[\x00-\x1F\x7F]', '', json_str)

def escape_json_config(config_file):
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
            clean_content = clean_control_characters(content)
            config = json.loads(clean_content)
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except json.JSONDecodeError as e:
        print(f"Error al procesar el archivo {config_file}: {e}")
    except Exception as e:
        print(f"Error inesperado al procesar el archivo {config_file}: {e}")


def process_config_files(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('_CONFIG.json'):
                config_file = os.path.join(subdir, file)
                escape_json_config(config_file)

def generate_markdown_list(root_dir):
    markdown_list = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(subdir, file)
                track, skill, module = get_levels(file_path, root_dir)
                file_type = get_file_type(file_path, subdir, file)
                lang = "ES" if file.endswith("_ES.md") else "PT" if file.endswith("_PT.md") else None
                
                titles = get_title(file_path, file_type)
                
                # Obtener la ruta del archivo de configuración correspondiente
                config_file = os.path.splitext(file_path.replace("_ES", "").replace("_PT", ""))[0] + "_CONFIG.json"
                config_data = read_config_data(config_file)
                
                if file_type == "container" and titles:
                    for title_dict in titles:
                        markdown_dict = {
                            "track": track,
                            "skill": skill,
                            "module": module,
                            "title": title_dict["title"],
                            "type": file_type,
                            "path": file_path[2:],
                            "lang": title_dict["lang"],
                            "difficulty": config_data.get("difficulty", ""),
                            "learning": config_data.get("learning", ""),
                            "time": config_data.get("time", ""),
                            "directions": config_data.get("directions", {}).get(title_dict["lang"], ""),
                            "discord_URL": config_data.get("discord_URL", {}).get(title_dict["lang"], "")
                        }
                        markdown_list.append(markdown_dict)
                else:
                    if titles:
                        markdown_dict = {
                            "track": track,
                            "skill": skill,
                            "module": module,
                            "title": titles[0]["title"],
                            "type": file_type,
                            "path": file_path[2:],
                            "lang": lang if lang else titles[0]["lang"],
                            "difficulty": config_data.get("difficulty", ""),
                            "learning": config_data.get("learning", ""),
                            "time": config_data.get("time", ""),
                            "directions": config_data.get("directions", {}).get(lang, ""),
                            "discord_URL": config_data.get("discord_URL", {}).get(lang, "")
                        }
                        markdown_list.append(markdown_dict)
                    else:
                        markdown_dict = {
                            "track": track,
                            "skill": skill,
                            "module": module,
                            "title": "Sin título",
                            "type": file_type,
                            "path": file_path[2:],
                            "lang": lang,
                            "difficulty": config_data.get("difficulty", ""),
                            "learning": config_data.get("learning", ""),
                            "time": config_data.get("time", ""),
                            "directions": config_data.get("directions", {}).get(lang, ""),
                            "discord_URL": config_data.get("discord_URL", {}).get(lang, "")
                        }
                        markdown_list.append(markdown_dict)
    return markdown_list

def read_config_data(config_file):
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}



def get_levels(file_path, root_dir):
    parts = os.path.relpath(file_path, root_dir).split(os.sep)
    if len(parts) < 3:
        return None, None, None
    return parts[0], parts[1], parts[2]

def get_file_type(file_path, subdir, file):
    if "activities" in subdir and file.endswith(".md") and not file.endswith("README.md"):
        return "activity"
    if "topics" in subdir and file.endswith(".md") and not file.endswith("README.md"):
        return "topic"
    if file.endswith("README.md"):
        return "container"

def get_title(file_path, file_type):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if file_type == "container":  # Para README.md
            titles = [line.strip() for line in content.split('##') if line.strip()]
            titles_dict = []
            for i, title in enumerate(titles[1:]):  # Ignoramos el título principal
                lang = "ES" if i == 0 else "PT"
                titles_dict.append({"title": title, "lang": lang})
            return titles_dict
        else:  # Para "activity" y "topic"
            title_match = re.search(r'#\s*(.+)', content)
            if title_match:
                return [{"title": title_match.group(1).strip(), "lang": "ES"}]  # Asumimos que es en español si no se especifica
            else:
                return [{"title": "Sin título", "lang": "ES"}]  # Retornar un título por defecto si no hay títulos


def save_to_csv(data, filename):
    fieldnames = ["track", "skill", "module", "title", "type", "lang", "path", "difficulty", "learning", "time", "directions", "discord_URL"]
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    root_dir = "."
    process_config_files(root_dir)
    markdown_list = generate_markdown_list(root_dir)
    save_to_csv(markdown_list, "markdown_files.csv")
    save_to_json(markdown_list, "markdown_files.json")
