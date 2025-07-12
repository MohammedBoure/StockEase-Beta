from utils.file_utils import read_json


settings = read_json("config/settings.json")
font_size = read_json("config/font_sizes.json")
theme = read_json("config/themes.json")[settings["theme"]]
language = read_json("config/language.json")[settings["language"]]
