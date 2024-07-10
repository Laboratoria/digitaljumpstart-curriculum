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
        "learning", "difficulty", "time", "path", "discord_URL", "slug"
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
                    "discord_URL": {"ES": None, "PT": None}
                })

                lang = get_lang(file)
                sequence = get_sequence(subdir, file, file_type)
                title = get_title(file_path, file_type)

                if file_type == "container":
                    titles = get_container_titles(file_path)
                    for i, t in enumerate(titles):
                        lang_key = "ES" if i == 0 else "PT"
                        slug = f"{track}-{skill}-{module}-{t}-{file_type}-{lang_key}".lower().replace(' ', '-')
                        markdown_list.append(create_entry(
                            track, skill, module, t, file_type, lang_key,
                            sequence, additional_info["learning"], additional_info["difficulty"],
                            additional_info["time"], file_path, additional_info["discord_URL"].get(lang_key, None), slug
                        ))
                else:
                    slug = f"{track}-{skill}-{module}-{title}-{file_type}-{lang}".lower().replace(' ', '-')
                    markdown_list.append(create_entry(
                        track, skill, module, title, file_type, lang,
                        sequence, additional_info["learning"], additional_info["difficulty"],
                        additional_info["time"], file_path, additional_info["discord_URL"].get(lang, None), slug
                    ))

    return markdown_list

def get_config_content(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def get_levels(file_path, root_dir):
    # Placeholder function to extract track, skill, and module from the file path
    # Implement your logic here
    return "track", "skill", "module"

def get_file_type(file_path, subdir, file):
    # Placeholder function to determine the file type
    # Implement your logic here
    return "type"

def get_lang(file):
    # Placeholder function to determine the language
    # Implement your logic here
    return "lang"

def get_sequence(subdir, file, file_type):
    # Placeholder function to determine the sequence
    # Implement your logic here
    return "sequence"

def get_title(file_path, file_type):
    # Placeholder function to determine the title
    # Implement your logic here
    return "title"

def get_container_titles(file_path):
    # Placeholder function to extract container titles
    # Implement your logic here
    return ["title1", "title2"]

def create_entry(track, skill, module, title, file_type, lang, sequence, learning, difficulty, time, path, discord_URL, slug):
    return {
        "track": track,
        "skill": skill,
        "module": module,
        "title": title,
        "type": file_type,
        "lang": lang,
        "sequence": sequence,
        "learning": learning,
        "difficulty": difficulty,
        "time": time,
        "path": path,
        "discord_URL": discord_URL,
        "slug": slug
    }

def save_to_csv(data, filename):
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
