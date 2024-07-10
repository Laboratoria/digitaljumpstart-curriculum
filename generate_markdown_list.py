import os
import json
import csv
import yaml
import logging
import uuid  # Importar el módulo uuid

# Configuración del logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_markdown_list(root_dir):
    markdown_list = []
    keys = [
        "track", "skill", "module", "title", "type", "lang", "sequence",
        "learning", "difficulty", "time", "path", "discord_URL", "id"
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
                additional_info = config_data.get(config_prefix, {
                    "difficulty": None,
                    "learning": None,
                    "time": None,
                    "discord_URL": None
                })

                lang = get_lang(file)
                sequence = get_sequence(subdir, file, file_type)
                title = get_title(file_path, file_type)

                unique_id = str(uuid.uuid4())  # Generar un identificador único

                if file_type == "container":
                    titles = get_container_titles(file_path)
                    for i, t in enumerate(titles):
                        lang_key = "ES" if i == 0 else "PT"
                        markdown_list.append(create_entry(
                            track, skill, module, t, file_type, lang_key,
                            sequence, additional_info, file_path, unique_id
                        ))
                else:
                    markdown_list.append(create_entry(
                        track, skill, module, title, file_type, lang,
                        sequence, additional_info, file_path, unique_id
                    ))

    return markdown_list

def create_entry(track, skill, module, title, file_type, lang, sequence, additional_info, path, unique_id):
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
        "discord_URL": additional_info.get("discord_URL"),
        "id": unique_id  # Añadir el identificador único a la entrada
    }

# El resto del script permanece igual

if __name__ == "__main__":
    root_dir = "."
    markdown_list = generate_markdown_list(root_dir)
    
    logging.info(f"Total markdown files: {len(markdown_list)}")
    
    save_to_csv(markdown_list, "markdown_files.csv")
    save_to_json(markdown_list, "markdown_files.json")
    save_to_yaml(markdown_list, "markdown_files.yaml")

    # Filtrar y guardar programas
    programs = filter_programs(markdown_list)
    save_to_csv(programs, "programs.csv")
    save_to_json(programs, "programs.json")
    save_to_yaml(programs, "programs.yml")

    # Filtrar y guardar skills
    skills = filter_skills(markdown_list)
    save_to_csv(skills, "skills.csv")
    save_to_json(skills, "skills.json")
    save_to_yaml(skills, "skills.yml")

    # Filtrar y guardar modulos
    modules = filter_modules(markdown_list)
    save_to_csv(modules, "modules.csv")
    save_to_json(modules, "modules.json")
    save_to_yaml(modules, "modules.yml")

    # Filtrar y guardar actividades
    activities = filter_activities(markdown_list)
    save_to_csv(activities, "activities.csv")
    save_to_json(activities, "activities.json")
    save_to_yaml(activities, "activities.yml")

    # Filtrar y guardar topics
    topics = filter_topics(markdown_list)
    save_to_csv(topics, "topics.csv")
    save_to_json(topics, "topics.json")
    save_to_yaml(topics, "topics.yml")

    logging.info("All files have been saved.")
