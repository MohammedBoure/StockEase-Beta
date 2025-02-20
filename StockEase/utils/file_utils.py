import json


def write_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)



def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

font_size  = read_json("config/font_sizes.json")
theme = read_json("config/themes.json")["dark"]