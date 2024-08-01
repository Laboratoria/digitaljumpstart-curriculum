import os
import json
import csv

def process_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            config = json.loads(content)
        return config
    except Exception as e:
        print(f"Error processing JSON file {file_path}: {e}")
        return {}

def generate_markdown_list(root_dir):
    markdown_list = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(subdir, file)
                track, skill, module = get_levels(file_path, root_dir)
                file_type = get_file_type(file_path, subdir, file)
                config_file = os.path.splitext(file_path)[0] + "_CONFIG.json"
                additional_info = {}
                if os.path.exists(config_file):
                    additional_info = process_json_file(config_file)
                if file_type == "container":
                    if skill is None and module is None:
                        file_type = "program"
                    elif skill and module:
                        file_type = "module"
                entry = {
                    "track": track,
                    "skill": skill,
                    "module": module,
                    "title": get_title(file_path),
                    "type": file_type,
                    "path": file_path[2:]
                }
                entry.update(additional_info)
                markdown_list.append(entry)
    return markdown_list

def get_levels(file_path, root_dir):
    parts = os.path.relpath(file_path, root_dir).split(os.sep)
    return parts[0], parts[1], parts[2] if len(parts) > 2 else None

def get_file_type(file_path, subdir, file):
    if "activities" in subdir and file.endswith(".md") and not file.endswith("README.md"):
        return "activity"
    if "topics" in subdir and file.endswith(".md") and not file.endswith("README.md"):
        return "topic"
    if file.endswith("README.md"):
        return "container"
    return "unknown"

def get_title(file_path):
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith("# "):
                    return line[2:].strip()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return None

def save_to_csv(data, filename):
    if not data:
        print(f"No data to write to {filename}")
        return
    keys = data[0].keys()
    try:
        with open(filename, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
    except Exception as e:
        print(f"Error saving CSV file {filename}: {e}")

def save_to_json(data, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving JSON file {filename}: {e}")

if __name__ == "__main__":
    root_dir = "."
    markdown_list = generate_markdown_list(root_dir)
    save_to_csv(markdown_list, "markdown_files.csv")
    save_to_json(markdown_list, "markdown_files.json")
