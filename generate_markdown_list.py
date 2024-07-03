import os
import json

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

if __name__ == "__main__":
    root_dir = "path/to/your/markdown/files"
    markdown_list = generate_markdown_list(root_dir)
    with open("markdown_list.json", "w") as f:
        json.dump(markdown_list, f, indent=2)
