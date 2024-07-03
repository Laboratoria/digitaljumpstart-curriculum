import os
import yaml
import json
import pandas as pd

repo_path = '.'

markdown_files = []

for root, dirs, files in os.walk(repo_path):
    for file in files:
        if file.endswith('.md'):
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, repo_path)
            markdown_files.append(relative_path)

with open('markdown_files.yaml', 'w') as yaml_file:
    yaml.dump(markdown_files, yaml_file)

with open('markdown_files.json', 'w') as json_file:
    json.dump(markdown_files, json_file, indent=4)

df = pd.DataFrame(markdown_files, columns=['Path'])
df.to_csv('markdown_files.csv', index=False)
