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
                track, skill, module = get_levels(file_path)
                markdown_list.append({
                    "path": file_path,
                    "title": get_header(file_path),
                    "track": track,
                    "skill": skill,
                    "module": module
                })
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

def save_to_json(data, filename):
    if not data:
        print(f"No data to write to {filename}")
        return
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def save_to_yaml(data, filename):
    if not data:
        print(f"No data to write to {filename}")
        return
    with open(filename, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

if __name__ == "__main__":
    root_dir = "path/to/your/markdown/files"
    markdown_list = generate_markdown_list(root_dir)
    
    save_to_csv(markdown_list, "markdown_files.csv")
    save_to_json(markdown_list, "markdown_files.json")
    save_to_yaml(markdown_list, "markdown_files.yaml")

# Git commands to add and commit the generated files if they have changed
os.system('git add markdown_files.csv markdown_files.json markdown_files.yaml')
os.system('git commit -m "Add generated markdown list" || echo "No changes to commit"')
os.system('git push origin main')
