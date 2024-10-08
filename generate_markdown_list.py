import os
import json
import re
import csv
import requests
import logging

def clean_control_characters(json_str):
    return re.sub(r'[\x00-\x1F\x7F]', '', json_str.replace('\\_', '_').replace(r'\\(?!["\\/bfnrtu])', r'\\\\'))

def escape_json_config(config_file):
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.loads(clean_control_characters(f.read()))  # Limpiar y cargar JSON en una sola línea
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error procesando el archivo {config_file}: {e}")

def process_config_files(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('_CONFIG.json'):
                escape_json_config(os.path.join(subdir, file))

def extract_preview(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        match = re.search(r'<!--\s*preview:start\s*-->(.*?)<!--\s*preview:end\s*-->', f.read(), re.DOTALL)
        return match.group(1).strip() if match else ""

def modify_activity_links(content, lang, track, skill, module):
    replacement_base = f"?lang={lang}&track={track or ''}&skill={skill or ''}&module={module or ''}"
    return re.sub(r"//PATH_TO_THIS_SCRIPT:\?lang=XX&track=XXX&skill=XXXXXX&module=XXXXXX//", replacement_base, content)

def generate_markdown_list(root_dir):
    markdown_list = []
    log_file = "modification_log.txt"
    
    with open(log_file, 'w', encoding='utf-8') as log:
        for subdir, _, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(subdir, file)
                if file.endswith(".md"):
                    track, skill, module = get_levels(file_path, root_dir)
                    file_type = get_file_type(file_path, subdir, file)
                    lang = "ES" if file.endswith("_ES.md") else "PT" if file.endswith("_PT.md") else None
                    titles = get_title(file_path)

                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if file_type == "activity":
                        modified_content = modify_activity_links(content, lang, track, skill, module)
                        try:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(modified_content)
                            log.write(f"Archivo modificado: {file_path}\n")
                        except Exception as e:
                            log.write(f"Error al escribir en el archivo {file_path}: {e}\n")
                    else:
                        log.write(f"Sin cambios en: {file_path}\n")
                    
                    config_file = os.path.splitext(file_path.replace("_ES", "").replace("_PT", ""))[0] + "_CONFIG.json"
                    config_data = read_config_data(config_file)
                    
                    discord_url = config_data.get("discord_URL", {}).get(lang, "")
                    if discord_url:
                        discord_channel_id, discord_message_id = discord_url.split('/')[-2:]
                    else:
                        discord_channel_id, discord_message_id = None, None

                    slug = f"{track or ''}{'-' + skill if skill else ''}{'-' + module if module else ''}-{os.path.splitext(file)[0]}"

                    directions = extract_preview(file_path) if file_type in ["program", "skill", "module"] else config_data.get("directions", {}).get(lang, "")

                    markdown_dict = {
                        "track": track,
                        "skill": skill,
                        "module": module,
                        "title": titles.get("title", "Sin título"),
                        "type": file_type,
                        "path": file_path[2:],  # Quitar "./" del comienzo de la ruta del archivo
                        "lang": lang or titles.get("lang"),
                        "difficulty": config_data.get("difficulty", ""),
                        "learning": config_data.get("learning", ""),
                        "time": config_data.get("time", ""),
                        "directions": directions,
                        "discord_URL": discord_url,
                        "discord_channel_id": discord_channel_id,
                        "discord_message_id": discord_message_id,
                        "slug": slug
                    }

                    path_parts = os.path.relpath(file_path, root_dir).split(os.sep)
                    if file_type == "program":
                        markdown_dict.update({"track": path_parts[0], "skill": None, "module": None})
                    elif file_type == "skill":
                        markdown_dict.update({"track": path_parts[0], "skill": path_parts[1], "module": None})
                    elif file_type == "module":
                        markdown_dict.update({"track": path_parts[0], "skill": path_parts[1], "module": path_parts[2]})

                    markdown_list.append(markdown_dict)
    
    print(f"Log de modificaciones creado en {log_file}")
    return markdown_list

def get_levels(file_path, root_dir):
    parts = os.path.relpath(file_path, root_dir).split(os.sep)
    return (parts[0], None, None) if len(parts) == 2 else (parts[0], parts[1], parts[2]) if len(parts) >= 3 else (None, None, None)

def get_file_type(file_path, subdir, file):
    if "topics" in subdir:
        return "topic"
    if "activities" in subdir and not file.endswith(("README_ES.md", "README_PT.md")):
        return "activity"
    depth = len(os.path.relpath(subdir, root_dir).split(os.sep))
    return "program" if depth == 1 else "skill" if depth == 2 else "module"

def get_title(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        match = re.search(r'#\s*(.+)', f.read())
        return {"title": match.group(1).strip(), "lang": "ES" if file_path.endswith("_ES.md") else "PT"} if match else {"title": "Sin título", "lang": "ES" if file_path.endswith("_ES.md") else "PT"}

def read_config_data(config_file):
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_data(data, filename, format="csv"):
    if format == "csv":
        fieldnames = ["track", "skill", "module", "title", "type", "lang", "path", "difficulty", "learning", "time", "directions", "discord_URL", "discord_channel_id", "discord_message_id", "slug"]
        with open(filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(data)
    elif format == "json":
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def send_data_to_endpoint(url, data):
    try:
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            logging.info("Data successfully sent to endpoint.")
        else:
            logging.error(f"Failed to send data to endpoint. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logging.error(f"Error sending data to endpoint: {e}")

if __name__ == "__main__":
    root_dir = "."
    process_config_files(root_dir)
    markdown_list = generate_markdown_list(root_dir)
    save_data(markdown_list, "markdown_files.csv", format="csv")
    save_data(markdown_list, "markdown_files.json", format="json")

    endpoint_url = "https://us-central1-laboratoria-prologue.cloudfunctions.net/dj-curriculum-get"
    if endpoint_url:
        send_data_to_endpoint(endpoint_url, markdown_list)
    else:
        logging.error("ENDPOINT_URL variable not set.")

    logging.info("All files have been saved and data sent to endpoint.")
