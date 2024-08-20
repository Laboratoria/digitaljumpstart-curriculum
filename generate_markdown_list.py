import os
import json
import re
import csv
import requests
import logging

def clean_control_characters(json_str):
    # Reemplazar caracteres de escape incorrectos
    json_str = json_str.replace('\\_', '_')
    # Eliminar caracteres de control y manejar caracteres de escape inválidos
    json_str = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', json_str)  # Escapar correctamente las barras invertidas
    return re.sub(r'[\x00-\x1F\x7F]', '', json_str)  # Eliminar caracteres de control

def escape_json_config(config_file):
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
            clean_content = clean_control_characters(content)  # Limpiar contenido del archivo JSON
            config = json.loads(clean_content)  # Cargar el contenido limpio como un objeto JSON
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)  # Escribir el objeto JSON limpio de nuevo en el archivo
    except json.JSONDecodeError as e:
        print(f"Error al procesar el archivo {config_file}: {e}")  # Manejar errores de decodificación JSON
    except Exception as e:
        print(f"Error inesperado al procesar el archivo {config_file}: {e}")  # Manejar cualquier otro error

def process_config_files(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('_CONFIG.json'):
                config_file = os.path.join(subdir, file)
                escape_json_config(config_file)  # Procesar cada archivo de configuración JSON

def extract_preview(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'<div id="preview">(.*?)</div>', content, re.DOTALL)
        return match.group(1).strip() if match else ""

import re

def modify_activity_links(content, lang, track, skill, module):
    # Patrón exacto para buscar la cadena específica en el contenido
    pattern = r"//PATH_TO_THIS_SCRIPT:\?lang=XX&track=XXX&skill=XXXXXX&module=XXXXXX//"
    
    # Crear el reemplazo dinámico basado en los valores actuales de lang, track, skill, y module
    replacement = f"?lang={lang}&track={track or ''}&skill={skill or ''}&module={module or ''}"
    
    # Reemplazar todas las ocurrencias del patrón en el contenido
    modified_content = re.sub(pattern, replacement, content)
    
    return modified_content

def generate_markdown_list(root_dir):
    markdown_list = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            if file.endswith(".md"):
                track, skill, module = get_levels(file_path, root_dir)
                file_type = get_file_type(file_path, subdir, file)
                lang = "ES" if file.endswith("_ES.md") else "PT" if file.endswith("_PT.md") else None
                
                titles = get_title(file_path, file_type)

                # Leer el contenido del archivo
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Modificar los enlaces si es un archivo de tipo "activity"
                if file_type == "activity" and "https://path_to_this_script/" in content:
                    modified_content = modify_activity_links(content, lang, track, skill, module)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(modified_content)

                # Obtener la ruta del archivo de configuración correspondiente
                config_file = os.path.splitext(file_path.replace("_ES", "").replace("_PT", ""))[0] + "_CONFIG.json"
                config_data = read_config_data(config_file)
                
                discord_url = config_data.get("discord_URL", {}).get(lang, "")
                discord_channel_id = discord_url.split('/')[-2] if discord_url else ""
                discord_message_id = discord_url.split('/')[-1] if discord_url else ""

                slug = f"{track or ''}{'-' + skill if skill else ''}{'-' + module if module else ''}-{os.path.splitext(file)[0]}"

                # Extraer contenido del div con id preview solo para archivos README
                if file_type in ["program", "skill", "module"]:
                    directions = extract_preview(file_path)
                else:
                    directions = config_data.get("directions", {}).get(lang, "")

                markdown_dict = {
                    "track": track,
                    "skill": skill,
                    "module": module,
                    "title": titles[0]["title"] if titles else "Sin título",
                    "type": file_type,
                    "path": file_path[2:],  # Quitar "./" del comienzo de la ruta del archivo
                    "lang": lang if lang else titles[0]["lang"],
                    "difficulty": config_data.get("difficulty", ""),
                    "learning": config_data.get("learning", ""),
                    "time": config_data.get("time", ""),
                    "directions": directions,  # Utilizar contenido extraído del div preview si aplica, o del JSON
                    "discord_URL": discord_url,
                    "discord_channel_id": discord_channel_id,
                    "discord_message_id": discord_message_id,
                    "slug": slug
                }

                # Ajustar track, skill y module según el tipo y longitud de path_parts
                path_parts = os.path.relpath(file_path, root_dir).split(os.sep)
                if file_type == "program" and len(path_parts) >= 1:
                    markdown_dict["track"] = path_parts[0]
                    markdown_dict["skill"] = None
                    markdown_dict["module"] = None
                elif file_type == "skill" and len(path_parts) >= 2:
                    markdown_dict["track"] = path_parts[0]
                    markdown_dict["skill"] = path_parts[1]
                    markdown_dict["module"] = None
                elif file_type == "module" and len(path_parts) >= 3:
                    markdown_dict["track"] = path_parts[0]
                    markdown_dict["skill"] = path_parts[1]
                    markdown_dict["module"] = path_parts[2]
                else:
                    # Manejar casos en los que no hay suficientes niveles en path_parts
                    markdown_dict["track"] = path_parts[0] if len(path_parts) > 0 else None
                    markdown_dict["skill"] = path_parts[1] if len(path_parts) > 1 else None
                    markdown_dict["module"] = path_parts[2] if len(path_parts) > 2 else None

                markdown_list.append(markdown_dict)
    return markdown_list


def get_levels(file_path, root_dir):
    # Obtener los niveles de la ruta del archivo
    parts = os.path.relpath(file_path, root_dir).split(os.sep)
    if len(parts) == 1:  # Primer nivel
        return None, None, None
    elif len(parts) == 2:  # Segundo nivel
        return parts[0], None, None
    elif len(parts) >= 3:  # Tercer nivel o más profundo
        return parts[0], parts[1], parts[2]
    return None, None, None

def get_file_type(file_path, subdir, file):
    if "topics" in subdir and file.endswith(".md"):
        return "topic"
    if "activities" in subdir and file.endswith(".md") and not file.endswith("README_ES.md") and not file.endswith("README_PT.md"):
        return "activity"
    if file.endswith("README_ES.md") or file.endswith("README_PT.md"):
        relative_path = os.path.relpath(subdir, root_dir)
        depth = len(relative_path.split(os.sep))
        if depth == 1:
            return "program"
        elif depth == 2:
            return "skill"
        elif depth == 3:
            return "module"
    return "module"  # Asumimos que los demás archivos .md son de tipo "module"

def get_title(file_path, file_type):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        title_match = re.search(r'#\s*(.+)', content)  # Busca el primer h1
        if title_match:
            return [{"title": title_match.group(1).strip(), "lang": "ES" if file_path.endswith("_ES.md") else "PT"}]
        else:
            return [{"title": "Sin título", "lang": "ES" if file_path.endswith("_ES.md") else "PT"}]

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
            logging.info("Data successfully sent to endpoint.")  # Datos enviados correctamente al endpoint
        else:
            logging.error(f"Failed to send data to endpoint. Status code: {response.status_code}, Response: {response.text}")  # Error al enviar datos
    except Exception as e:
        logging.error(f"Error sending data to endpoint: {e}")  # Manejar cualquier otro error al enviar datos

if __name__ == "__main__":
    root_dir = "."
    process_config_files(root_dir)  # Procesar archivos de configuración
    markdown_list = generate_markdown_list(root_dir)  # Generar lista de archivos Markdown
    save_to_csv(markdown_list, "markdown_files.csv")  # Guardar la lista en un archivo CSV
    save_to_json(markdown_list, "markdown_files.json")  # Guardar la lista en un archivo JSON

    # Enviar datos al endpoint
    endpoint_url = "https://us-central1-laboratoria-prologue.cloudfunctions.net/dj-curriculum-get" 
    if endpoint_url:
        send_data_to_endpoint(endpoint_url, markdown_list)
    else:
        logging.error("ENDPOINT_URL variable not set.")  # Error si la URL del endpoint no está configurada

    logging.info("All files have been saved and data sent to endpoint.")  # Información de que todos los archivos han sido guardados y los datos enviados
