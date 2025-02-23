import json
import os


def write_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)



def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Get project root directory
CONFIG_PATH = os.path.join(BASE_DIR, "config")  # Path to config folder

font_size = read_json(os.path.join(CONFIG_PATH, "font_sizes.json"))
theme = read_json(os.path.join(CONFIG_PATH, "themes.json"))["light"]