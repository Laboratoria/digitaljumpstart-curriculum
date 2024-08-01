import os
import json
import re
import csv
import requests
import logging

def clean_control_characters(json_str):
    json_str = json_str.replace('\\_', '_')
    json_str = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', json_str)
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

def duplicate_readme_files(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file == "README.md":
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                es_file_path = os.path.join(subdir, "README_ES.md")
                pt_file_path = os.path.join(subdir, "README_PT.md")
                with open(es_file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                with open(pt_file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

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
                
                config_file = os.path.splitext(file_path.replace("_ES", "").replace("_PT", ""))[0] + "_CONFIG.json"
                config_data = read_config_data(config_file)
                
                discord_url = config_data.get("discord_URL", {}).get(lang, "")
                discord_channel_id = discord_url.split('/')[-2] if discord_url else ""
                discord_message_id = discord_url.split('/')[-1] if discord_url else ""

                slug = f"{track or ''}{'-' + skill if skill else ''}{'-' + module if module else ''}-{os.path.splitext(file)[0]}"

                if file_type == "container" and titles:
                    for title_dict in titles:
                        markdown_dict = {
                            "track": track,
                            "skill": skill,
                            "module": module,
                            "title": title_dict["title"],
                            "type": "module",
                            "path": file_path[2:],
                            "lang": title_dict["lang"],
                            "difficulty": config_data.get("difficulty", ""),
                            "learning": config_data.get("learning", ""),
                            "time": config_data.get("time", ""),
                            "directions": config_data.get("directions", {}).get(title_dict["lang"], ""),
                            "discord_URL": discord_url,
                            "discord_channel_id": discord_channel_id,
                            "discord_message_id": discord_message_id,
                            "slug": slug
                        }
                        path_parts = file_path.split(os.sep)
                        if "README.md" in file_path:
                            if len(path_parts) == 2:
                                markdown_dict["track"] = None
                                markdown_dict["skill"] = None
                                markdown_dict["module"] = None
                                markdown_dict["type"] = "program"
                            elif len(path_parts) == 3:
                                markdown_dict["type"] = "program"
                                markdown_dict["skill"] = path_parts[1]
                                markdown_dict["module"] = None
                            elif len(path_parts) == 4:
                                markdown_dict["type"] = "skill"
                                markdown_dict["skill"] = path_parts[1]
                                markdown_dict["module"] = path_parts[2]
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
                            "discord_URL": discord_url,
                            "discord_channel_id": discord_channel_id,
                            "discord_message_id": discord_message_id,
                            "slug": slug
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
                            "discord_URL": discord_url,
                            "discord_channel_id": discord_channel_id,
                            "discord_message_id": discord_message_id,
                            "slug": slug
                        }
                        markdown_list.append(markdown_dict)
    return markdown_list

def get_levels(file_path, root_dir):
    parts = os.path.relpath(file_path, root_dir).split(os.sep)
    if len(parts) == 1:  # Primer nivel
        return None, None, None
    elif len(parts) == 2:  # Segundo nivel
        return parts[0], None, parts[1]
    elif len(parts) >= 3:  # Tercer nivel o más profundo
        return parts[0], parts[1], parts[2]
    return None, None, None

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

def read_config_data(config_file):
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_to_csv(data, filename):
    fieldnames = ["track", "skill", "module", "title", "type", "lang", "path", "difficulty", "learning", "time", "directions", "discord_URL", "discord_channel_id", "discord_message_id", "slug"]
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def send_data_to_endpoint(url, data):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            logging.info("Data successfully sent to endpoint.")
        else:
            logging.error(f"Failed to send data to endpoint. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logging.error(f"Error sending data to endpoint: {e}")
