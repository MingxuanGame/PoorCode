"""
This is a module for reading recipe files
Here are some ways:
    -


这是关于读取配方文件的模块
这是一些方法：
    -
"""
import difflib
import json
import os

from PIL import Image


def read_recipe(name: str, data_path: str) -> [dict, None]:
    with open(os.path.join(data_path, "minecraft", "index.json"), "r", encoding="utf-8") as f:
        index: dict = json.loads(f.read())
    try:
        entry = index[name]
        with open(os.path.join(data_path, "minecraft", "recipes", entry + ".json"), "r", encoding="utf-8") as f:
            recipe = json.loads(f.read())
        recipe["result"] = entry
        return recipe
    except KeyError:
        return None
    except FileNotFoundError:
        return None


def read_recipe_image(name: str, save_file: str, data_path: str) -> None:
    coordinate = {
        "crafting_table": {
            "input": [
                (30, 17), (48, 17), (66, 17), (30, 35), (48, 35), (66, 35), (30, 53), (48, 53), (66, 53)
            ],
            "output": (124, 35),
            "identifier": (150, 8)
        },
        "smoker": {
            "input": (56, 17),
            "output": (116, 35),
            "fuel": (56, 53)
        },
        "grindstone": {
            "input": [
                (48, 18),
                (48, 40)
            ],
            "output": (128, 34)
        },
        "smithing": {
            "input": (27, 47),
            "material": (76, 47),
            "output": (134, 47)
        }
    }

    recipe: dict = read_recipe(name, data_path)
    if recipe is not None:
        if recipe["type"] == 'minecraft:crafting_shaped' or recipe["type"] == "minecraft:crafting_shapeless":
            background = Image.open(os.path.join(data_path, "minecraft", "gui", "crafting_table.png"))
            for i in range(1, 10):
                try:
                    if recipe["recipe"][f"{i}"] is not None:
                        item = recipe["recipe"][f"{i}"][0]
                        textures_list = os.listdir(os.path.join(data_path, "minecraft", "textures"))
                        for textures_file in textures_list:
                            if item[10:] + ".png" == textures_file:
                                file = os.path.join(data_path, "minecraft", "textures", f"{item[10:]}.png")
                            elif item[10:] in textures_file and \
                                    difflib.SequenceMatcher(None, item[10:], textures_file).quick_ratio() >= 0.7:
                                file = os.path.join(data_path, "minecraft", "textures", f"{item[10:]}_00.png")
                            else:
                                continue
                            material = Image.open(file).convert("RGBA")
                            background.paste(material, coordinate["crafting_table"]["input"][i - 1], material)
                        for textures_file in textures_list:
                            if recipe["result"] + ".png" == textures_file:
                                result = os.path.join(data_path, "minecraft", "textures", f"{recipe['result']}.png")
                            elif recipe["result"] in textures_file:
                                result = os.path.join(data_path, "minecraft", "textures", f"{recipe['result']}_00.png")
                            else:
                                continue
                            output = Image.open(result).convert("RGBA")
                            background.paste(output, coordinate["crafting_table"]["output"], output)
                except KeyError:
                    continue
            pass

        # if recipe["count"] > 1:


"""
   Copyright 2021 MingxuanGame

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
