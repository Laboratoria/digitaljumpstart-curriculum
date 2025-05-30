import os
import json
import re
import csv
import requests
import logging

# --- Utilidades para limpiar y procesar JSON de configuración ---

def clean_control_characters(json_str):
    return re.sub(r'[\x00-\x1F\x7F]', '', json_str.replace('\\_', '_').replace(r'\\(?!["\\/bfnrtu])', r'\\\\'))

def escape_json_config(config_file):
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.loads(clean_control_characters(f.read()))
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error procesando el archivo {config_file}: {e}")

def process_config_files(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('_CONFIG.json'):
                escape_json_config(os.path.join(subdir, file))

# --- Funciones para procesar el contenido de los archivos ---

def extract_preview(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'<!--\s*preview:start\s*-->(.*?)<!--\s*preview:end\s*-->', content, re.DOTALL)
        return match.group(1).strip() if match else ""

def modify_activity_links(content, lang, track, skill, module):
    replacement_base = f"?lang={lang}&track={track or ''}&skill={skill or ''}&module={module or ''}"
    return re.sub(r"//PATH_TO_THIS_SCRIPT:\?lang=XX&track=XXX&skill=XXXXXX&module=XXXXXX//", replacement_base, content)

# --- Funciones para extraer niveles y determinar el tipo, usando estructura unificada ---

def get_levels(file_path, root_dir):
    """
    Se asume que la ruta relativa tiene esta forma:
      - Para TRACKS: TRACKS/<track_id>/<skill>/<module>/... (con posible carpeta de actividades)
      - Para COURSES: COURSES/<track_id>/<course_id>/<module>/... 
    Devuelve (track, skill, module) extraídos de posiciones fijas.
    """
    parts = os.path.relpath(file_path, root_dir).split(os.sep)
    cat = parts[0].upper()  # "TRACKS" o "COURSES"
    if cat in ["TRACKS", "COURSES"]:
        track = parts[1] if len(parts) > 1 else None
        skill = parts[2] if len(parts) > 2 else None
        module = parts[3] if len(parts) > 3 else None
        return (track, skill, module)
    else:
        return (parts[0], parts[1] if len(parts) > 1 else None, parts[2] if len(parts) > 2 else None)

def get_file_type(file_path, subdir, file):
    """
    Determina el tipo de archivo basándose en la estructura de la ruta.
    Se usa la cantidad de elementos (parts) para diferenciar:
      Para TRACKS:
         - len(parts)==3: e.g. TRACKS/LEA/README_ES.md           -> "program"
         - len(parts)==4: e.g. TRACKS/LEA/01_intro/README_ES.md       -> "skill"
         - len(parts)==5: e.g. TRACKS/LEA/01_intro/02_mechanics/README_ES.md -> "module"
      Para COURSES:
         - len(parts)==3: e.g. COURSES/ZENDESK_01/README_ES.md         -> "course"
         - len(parts)==4: e.g. COURSES/ZENDESK/01_zendesk_01/README_ES.md  -> "skill"
         - len(parts)==5: e.g. COURSES/ZENDESK/01_zendesk_01/01_modulo_01/README_ES.md -> "module"
      Además, si el archivo está en una carpeta de actividades y no es README, se asigna "activity".
    """
    parts = os.path.relpath(file_path, root_dir).split(os.sep)
    cat = parts[0].upper()
    
    # Si se trata de una actividad (archivo no README dentro de carpeta "activities" o "activity")
    if "ACTIVITIES" in subdir.upper() or "ACTIVITY" in subdir.upper():
        if not file.startswith("README"):
            return "activity"
    
    if cat == "TRACKS":
        if len(parts) == 3 and file.startswith("README"):
            return "program"    # Ej: TRACKS/LEA/README_ES.md
        elif len(parts) == 4 and file.startswith("README"):
            return "skill"      # Ej: TRACKS/LEA/01_intro/README_ES.md
        elif len(parts) >= 5 and file.startswith("README"):
            return "module"     # Ej: TRACKS/LEA/01_intro/02_mechanics/README_ES.md
    elif cat == "COURSES":
        if len(parts) == 3 and file.startswith("README"):
            return "course"     # Ej: COURSES/ZENDESK_01/README_ES.md
        elif len(parts) == 4 and file.startswith("README"):
            return "skill"      # Ej: COURSES/ZENDESK/01_zendesk_01/README_ES.md
        elif len(parts) == 5 and file.startswith("README"):
            return "module"     # Ej: COURSES/ZENDESK/01_zendesk_01/01_modulo_01/README_ES.md
        elif len(parts) >= 6 and file.startswith("README"):
            return "module"
    
    # Caso por defecto: usar la profundidad del directorio
    depth = len(os.path.relpath(subdir, root_dir).split(os.sep))
    return "program" if depth == 1 else "skill" if depth == 2 else "module"

def get_title(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'#\s*(.+)', content)
        lang = "ES" if file_path.endswith("_ES.md") else "PT"
        return {"title": match.group(1).strip() if match else "Sin título", "lang": lang}

def read_config_data(config_file):
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

# --- Generación de la lista de archivos Markdown ---

def generate_markdown_list(root_dir):
    markdown_list = []
    log_file = "modification_log.txt"
    
    with open(log_file, 'w', encoding='utf-8') as log:
        for subdir, _, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(subdir, file)
                if file.endswith(".md"):
                    parts = os.path.relpath(file_path, root_dir).split(os.sep)
                    cat = parts[0].upper()
                    (track, skill, module) = get_levels(file_path, root_dir)
                    
                    file_type = get_file_type(file_path, subdir, file)
                    lang = "ES" if file.endswith("_ES.md") else "PT" if file.endswith("_PT.md") else None
                    titles = get_title(file_path)
                    
                    with open(file_path, 'r', encoding='utf-8') as f_obj:
                        content = f_obj.read()
                    
                    if file_type == "activity":
                        modified_content = modify_activity_links(content, lang, track, skill, module)
                        try:
                            with open(file_path, 'w', encoding='utf-8') as f_obj:
                                f_obj.write(modified_content)
                            log.write(f"Archivo modificado: {file_path}\n")
                        except Exception as e:
                            log.write(f"Error al escribir en {file_path}: {e}\n")
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
                    
                    directions = (extract_preview(file_path)
                                  if file_type in ["program", "course", "skill", "module"]
                                  else config_data.get("directions", {}).get(lang, ""))
                    
                    markdown_dict = {
                        "track": track,
                        "skill": skill,
                        "module": module,
                        "title": titles.get("title", "Sin título"),
                        "type": file_type,
                        "path": file_path[2:],  # Quitar "./" inicial si existe
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
                    
                    # Para contenidos que no sean de TRACKS o COURSES, se puede actualizar según la profundidad
                    if cat not in ["TRACKS", "COURSES"]:
                        if file_type == "program":
                            markdown_dict.update({"track": parts[0], "skill": None, "module": None})
                        elif file_type == "skill":
                            markdown_dict.update({"track": parts[0], "skill": parts[1], "module": None})
                        elif file_type == "module":
                            markdown_dict.update({"track": parts[0], "skill": parts[1], "module": parts[2]})
                    
                    markdown_list.append(markdown_dict)
    
    print(f"Log de modificaciones creado en {log_file}")
    return markdown_list

def save_data(data, filename, format="csv"):
    if format == "csv":
        fieldnames = ["track", "skill", "module", "title", "type", "lang", "path", "difficulty",
                      "learning", "time", "directions", "discord_URL", "discord_channel_id",
                      "discord_message_id", "slug"]
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

# --- Bloque principal ---

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
