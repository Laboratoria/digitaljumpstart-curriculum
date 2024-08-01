import os
import json
import csv

def escape_json_config(config_file):
    with open(config_file, 'r') as f:
        content = f.read().replace('\\', '\\\\')
        config = json.loads(content, strict=False)
    config['directions'] = config['directions'].replace('\\', '\\\\')
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

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
                config_file = os.path.splitext(file_path)[0] + "_CONFIG.json"
                if os.path.exists(config_file):
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                        additional_info = {}
                        if "directions" in config and isinstance(config["directions"], dict):
                            if file.endswith("_ES.md"):
                                additional_info["directions"] = config["directions"].get("ES", "")
                                additional_info["discord_URL"] = config["discord_URL"].get("ES", "")
                            elif file.endswith("_PT.md"):
                                additional_info["directions"] = config["directions"].get("PT", "")
                                additional_info["discord_URL"] = config["discord_URL"].get("PT", "")
                        else:
                            additional_info["directions"] = config.get("directions", "")
                            additional_info["discord_URL"] = config.get("discord_URL", "")
                        additional_info["difficulty"] = config.get("difficulty")
                        additional_info["learning"] = config.get("learning")
                        additional_info["time"] = config.get("time")
                else:
                    additional_info = {}
                if file_type == "container":
                    if skill is None and module is None:
                        file_type = "program"
                    elif skill and module:
                        file_type = "module"
                markdown_dict = {
                    "track": track,
                    "skill": skill,
                    "module": module,
                    "title": get_title(file_path),
                    "type": file_type,
                    "path": file_path[2:]
                }
                markdown_dict.update(additional_info)
                markdown_list.append(markdown_dict)
    return markdown_list

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

def get_title(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("# "):
                return line[2:].strip()
    return None

def save_to_csv(data, filename):
    fieldnames = ["track", "skill", "module", "title", "type", "path", "difficulty", "learning", "time", "directions", "discord_URL"]
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    root_dir = "."
    process_config_files(root_dir)
    markdown_list = generate_markdown_list(root_dir)
    save_to_csv(markdown_list, "markdown_files.csv")
    save_to_json(markdown_list, "markdown_files.json")
