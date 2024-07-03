import os
import json
import csv
import yaml

def generate_markdown_list(root_dir):
    markdown_list = []
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(subdir, file)
                print(f"Processing file: {file_path}")  # Debugging
                track, skill, module = get_levels(file_path)
                markdown_list.append({
                    "path": file_path,
                    "title": get_header(file_path),
                    "track": track,
                    "skill": skill,
                    "module": module
                })
    print(f"Markdown files found: {len(markdown_list)}")  # Debugging
    return markdown_list

def get_header(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("# "):
                return line[2:].strip()
    return None

def get_levels(file_path):
    parts = file_path.split(os.sep)
    if len(parts) >= 4:
        return parts[-4], parts[-3], parts[-2]
    return None, None, None

def save_to_csv(data, filename):
    if not data:
        print(f"No data to write to {filename}")
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"CSV file saved: {filename}")  # Debugging

def save_to_json(data, filename):
    if not data:
        print(f"No data to write to {filename}")
        return
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"JSON file saved: {filename}")  # Debugging

def save_to_yaml(data, filename):
    if not data:
        print(f"No data to write to {filename}")
        return
    with open(filename, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
    print(f"YAML file saved: {filename}")  # Debugging

if __name__ == "__main__":
    root_dir = "path/to/your/markdown/files"  # Make sure this path is correct
    markdown_list = generate_markdown_list(root_dir)

    save_to_csv(markdown_list, "markdown_files.csv")
    save_to_json(markdown_list, "markdown_files.json")
    save_to_yaml(markdown_list, "markdown_files.yaml")
