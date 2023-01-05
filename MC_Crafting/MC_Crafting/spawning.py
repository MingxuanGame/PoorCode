r"""
This is a module for spawning recipe files
Here are some ways:
    - "spawn_recipes_file" to generate the recipe file


这是关于生成配方文件的模块
这是一些方法：
    - ”spawn_recipes_file“ 生成配方文件
"""
import json
import os
import shutil
import sys
import urllib.request
import zipfile

from PIL import Image
from colorama import Fore, init


def spawn_recipes_file(file: str, cache_path: str = "cache", data_path: str = "data", assets_path: str = None) -> int:
    """
    Spawn recipes files | 生成配方文件

    :param assets_path: Minecraft client "assets" path | 《我的世界》客户端assets目录
    :type cache_path: str
    :type data_path: str
    :type file: str
    :param file: Minecraft client(Server) ".jar" file | 《我的世界》客户端（服务端）的.jar文件
    :param cache_path: Cache folder path | 缓存文件夹目录
    :param data_path: Data folder path | 数据文件夹目录
    :return: Returns 0 and -1 when an exception occurs | 返回0，当发生异常时返回-1
    """
    _INFO = "INFO"
    _WARN = "WARN"
    _ERROR = "ERROR"
    _SUCCESS = "SUCCESS"
    if sys.platform == "win32":
        # Windows OS
        init(autoreset=True, wrap=True)
    try:
        print(Fore.WHITE + f"[Spawning-Thread/{_INFO}] Start spawning recipe file | 开始生成配方文件")

        if not os.path.exists(cache_path):
            os.mkdir(cache_path)
        else:
            if len(os.listdir(cache_path)) > 0:
                is_delete_dir = input(
                    Fore.LIGHTYELLOW_EX + f"[Spawning-Thread/{_WARN}] Cache folder already exists, "
                                          f"Whether empty and rebuild? |"
                                          f" 已存在缓存文件夹，是否清空并重建 ({os.path.join(os.getcwd(), cache_path)})[y/n]").lower()
                while True:
                    if is_delete_dir == "y":
                        print(Fore.WHITE + f"[Spawning-Thread/{_INFO}] Start to empty the cache folder (it "
                                           f"will take a long time if there is too much content) | "
                                           f"开始清空缓存文件夹（如果内容较多需要较长时间）")
                        shutil.rmtree(cache_path)
                        os.mkdir(cache_path)
                        print(Fore.GREEN + f"[Spawning-Thread/{_SUCCESS}] Empty cache folder complete | 清空缓存文件夹完成")
                        break
                    elif is_delete_dir == "n":
                        return 0
                    else:
                        is_delete_dir = input(Fore.LIGHTYELLOW_EX + f"[Spawning-Thread/{_WARN}] Please input [y/n]"
                                                                    f" | 请输入[y/n]").lower()

        print(Fore.WHITE + f"[Spawning-Thread/{_INFO}] Start analyzing the core | 开始分析核心"
                           f"({os.path.join(os.getcwd(), file)})")
        core_file_open = zipfile.ZipFile(file)
        file_list = core_file_open.namelist()
        if "data/.mcassetsroot" not in file_list:
            print((Fore.WHITE + f"[Spawning-Thread/{_INFO}] The core does not meet the requirements and has "
                                f"been withdrawn | 核心不符合，已经退出"))
            core_file_open.close()
            return 0

        print(
            Fore.WHITE + f"[Spawning-Thread/{_INFO}] Start unpacking core | 开始解压核心({os.path.join(os.getcwd(), file)})")
        for file in file_list:
            if file[0:22] == "data/minecraft/recipes" or file[0:39] == "assets/minecraft/textures/gui/container" \
                    or file[0:30] == "assets/minecraft/textures/item" or file == "assets/minecraft/lang/en_us.json":
                core_file_open.extract(file, cache_path)
        core_file_open.close()
        print(Fore.GREEN + f"[Spawning-Thread/{_SUCCESS}] Unpacking core complete | 解压核心完成")
        print(Fore.WHITE + f"[Spawning-Thread/{_INFO}] Start writing cache to data file | 开始将缓存写入数据文件"
                           f"({os.path.join(os.getcwd(), data_path)})")
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        else:
            if len(os.listdir(data_path)) > 0:
                is_delete_dir = input(
                    Fore.LIGHTYELLOW_EX + f"[Spawning-Thread/{_WARN}] Data folder already exists, Whether empty and "
                                          f"rebuild? | "
                                          f"已存在数据文件夹，是否清空并重建？({os.path.join(os.getcwd(), data_path)})[y/n]").lower()
                while True:
                    if is_delete_dir == "y":
                        print(Fore.WHITE + f"[Spawning-Thread/{_INFO}] Start emptying the data folder (it "
                                           f"will take a long time if there are many contents) "
                                           f" | 开始清空数据文件夹（如果内容较多需要较长时间）")
                        shutil.rmtree(data_path)
                        os.mkdir(data_path)
                        print(Fore.GREEN + f"[Spawning-Thread/{_SUCCESS}] Empty data folder complete "
                                           f"| 清空数据文件夹完成")
                        break
                    elif is_delete_dir == "n":
                        return 0
                    else:
                        is_delete_dir = input(Fore.LIGHTYELLOW_EX + f"[Spawning-Thread/{_WARN}] Please input [y/n]"
                                                                    f" | 请输入[y/n]").lower()
        recipes_dir = os.listdir(os.path.join(cache_path, "data", "minecraft", "recipes"))
        assets_gui_dir = os.listdir(os.path.join(cache_path, "assets", "minecraft", "textures", "gui", "container"))
        assets_item_dir = os.listdir(os.path.join(cache_path, "assets", "minecraft", "textures", "item"))
        os.makedirs(os.path.join(data_path, "minecraft", "recipes"))
        os.mkdir(os.path.join(data_path, "minecraft", "textures"))
        os.mkdir(os.path.join(data_path, "minecraft", "gui"))
        os.mkdir(os.path.join(data_path, "minecraft", "lang"))
        for recipe_file in recipes_dir:
            with open(os.path.join(cache_path, "data", "minecraft", "recipes", recipe_file), "r",
                      encoding="utf-8") as f:
                recipe = json.loads(f.read())
            recipe_json = {
                "recipe": {}
            }
            if recipe["type"] == "minecraft:crafting_shaped":
                if len(recipe["pattern"]) == 1:
                    for i in range(4, 10):
                        recipe_json["recipe"][str(i)] = None
                elif len(recipe["pattern"]) == 2:
                    for i in range(7, 10):
                        recipe_json["recipe"][str(i)] = None
                recipe_key = "".join(recipe["pattern"])
                for i in range(len(recipe_key)):
                    if recipe_key[i] == " ":
                        recipe_json["recipe"][str(i + 1)] = None
                    else:
                        if type(recipe["key"][recipe_key[i]]) is list:
                            items = []
                            for item in recipe["key"][recipe_key[i]]:
                                items.append(item["item"])
                            recipe_json["recipe"][str(i + 1)] = items
                        else:
                            try:
                                recipe_json["recipe"][str(i + 1)] = [recipe["key"][recipe_key[i]]["item"]]
                            except KeyError:
                                recipe_json["recipe"][str(i + 1)] = [recipe["key"][recipe_key[i]]["tag"]]
            elif recipe["type"] == "minecraft:crafting_shapeless":
                for i in range(len(recipe["ingredients"])):
                    if type(recipe["ingredients"][i]) is list:
                        items = []
                        for item in recipe["ingredients"][i]:
                            items.append(item["item"])
                        recipe_json["recipe"][str(i + 1)] = items
                    else:
                        try:
                            recipe_json["recipe"][str(i + 1)] = recipe["ingredients"][i]["item"]
                        except KeyError:
                            recipe_json["recipe"][str(i + 1)] = recipe["ingredients"][i]["tag"]
                for i in range(10 - len(recipe["ingredients"]), 10):
                    recipe_json["recipe"][str(i)] = None
            elif recipe["type"] == "smelting" or recipe["type"] == "stonecutting":
                if type(recipe["ingredient"]) is list:
                    items = []
                    for item in recipe["ingredient"]:
                        items.append(item["item"])
                    recipe_json["recipe"]["1"] = items
                else:
                    recipe_json["recipe"]["1"] = recipe["ingredient"]["item"]
            elif recipe["type"] == "smithing":
                recipe_json["recipe"]["1"] = recipe["base"]["item"]
                recipe_json["recipe"]["2"] = recipe["addition"]["item"]
            else:
                print(Fore.WHITE + f"[Spawning-Thread/{_INFO}] Read {recipe_file}...Ignore"
                                   f" | 读取{recipe_file}......忽略")
                continue
            if "count" in recipe["result"]:
                recipe_json["count"] = recipe["result"]["count"]
            else:
                recipe_json["count"] = 1
            recipe_json["type"] = recipe["type"]
            recipe_result_file = recipe["result"]["item"][10:] + ".json"
            if recipe_result_file in os.listdir(os.path.join(data_path, "minecraft")):
                for i in range(1, 1024):
                    recipe_result_file = recipe["result"]["item"][10:] + f"_{str(i)}.json"
                    if recipe_result_file not in os.listdir(os.path.join(data_path, "minecraft")):
                        break
            recipe_result_file = os.path.join(data_path, "minecraft", "recipes", recipe_result_file)
            with open(recipe_result_file, "w", encoding="utf-8") as f:
                f.write(json.dumps(recipe_json, ensure_ascii=False, sort_keys=True, indent=2))
            print(Fore.WHITE + f"[Spawning-Thread/{_INFO}] Read {recipe_file}...Write as {recipe_result_file} /"
                               f" 读取{recipe_file}......写入为{recipe_result_file}")

        for asset_file in assets_item_dir:
            shutil.copy(os.path.join(cache_path, "assets", "minecraft", "textures", "item", asset_file),
                        os.path.join(data_path, "minecraft", "textures"))
            print(Fore.WHITE + f'[Spawning-Thread/{_INFO}] Copy {asset_file} to '
                               f'{os.path.join(data_path, "minecraft", "textures", f"{asset_file}")} | '
                               f'复制{asset_file}到{os.path.join(data_path, "minecraft", "textures", f"{asset_file}")}')

        for gui_file in assets_gui_dir:
            if gui_file in ["crafting_table.png", "smoker.png", "grindstone.png", "smithing.png"]:
                gui = Image.open(os.path.join(cache_path, "assets", "minecraft", "textures", "gui",
                                              "container", gui_file))
                box = (0, 0, 176, 83)
                region = gui.crop(box)
                gui.close()
                region.save(os.path.join(data_path, "minecraft", "gui", gui_file))
                print(Fore.WHITE + f'[Spawning-Thread/{_INFO}] Copy {gui_file} to '
                                   f'{os.path.join(data_path, "minecraft", "textures", f"{gui_file}")} | '
                                   f'复制{gui_file}到{os.path.join(data_path, "minecraft", "gui", f"{gui_file}")}')
        if not os.path.exists("identifier.png"):
            url = "http://mingxuangame.top/MC_Crafting.png"
            print(Fore.WHITE + f'[Spawning-Thread/{_INFO}] Not found "identifier.png", will downloading '
                               f'from {url} | identifier.png缺失，将从 {url} 下载')
            with open("identifier.png", 'wb') as f:
                f.write(urllib.request.urlopen(url).read())
            print(Fore.GREEN + f'[Spawning-Thread/{_SUCCESS}] Downloading "identifier.png...Done" | '
                               f'下载identifier.png......完成')
        shutil.move("identifier.png", os.path.join(data_path, "minecraft", "gui"))
        print(Fore.WHITE + f'[Spawning-Thread/{_INFO}] Move identifier.png to '
                           f'{os.path.join(data_path, "minecraft", "textures", f"identifier.png")} | '
                           f'移动identifier.png到{os.path.join(data_path, "minecraft", "gui", f"identifier.png")}')

        print(Fore.WHITE + f'[Spawning-Thread/{_INFO}] Start to write index file, this step takes a long time, '
                           f'please wait patiently / 开始写入索引文件，此步需要时间较长，请耐心等候')
        with open(os.path.join(cache_path, "assets", "minecraft", "lang", "en_us.json"), "r", encoding="utf-8") as f:
            lang_file: dict = json.loads(f.read())
        lang = {}
        for key in lang_file.keys():
            key = key.strip("\n")
            if "%s" in lang_file[key]:
                continue
            if key[0:15] == "block.minecraft":
                lang[lang_file[key]] = key[16:]
            elif key[0:14] == "item.minecraft":
                lang[lang_file[key]] = key[15:]
        if assets_path is not None:
            max_version = float(os.listdir(os.path.join(assets_path, "indexes"))[0][:-5])
            for version in os.listdir(os.path.join(assets_path, "indexes")):
                if float(version[:-5]) > max_version:
                    max_version = version[:-5]
            with open(os.path.join(assets_path, "indexes", str(max_version) + ".json"), "r", encoding="utf-8") as f:
                other_lang_index: dict = json.loads(f.read())["objects"]
            other_lang_list = []
            other_lang_files = []
            for key in other_lang_index.keys():
                key = key.strip("\n")
                if "minecraft/lang" in key:
                    other_lang_list.append(other_lang_index[key]["hash"])
            for root, _, files in os.walk(os.path.join(assets_path, "objects"), topdown=False):
                for name in files:
                    if os.path.isfile(os.path.join(root, name)):
                        for other_lang in other_lang_list:
                            if other_lang in os.path.join(root, name):
                                other_lang_files.append(os.path.join(root, name))
            for other_lang_json in other_lang_files:
                with open(other_lang_json, "r", encoding="utf-8") as f:
                    other_lang_json_text = json.loads(f.read())
                for key in other_lang_json_text.keys():
                    if "%s" in other_lang_json_text[key]:
                        continue
                    if key[0:15] == "block.minecraft":
                        lang[other_lang_json_text[key]] = key[16:]
                    elif key[0:14] == "item.minecraft":
                        lang[other_lang_json_text[key]] = key[15:]
            del other_lang_files, other_lang_list, other_lang_index, other_lang
        with open(os.path.join(data_path, "minecraft", "index.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(lang, ensure_ascii=False, sort_keys=True, indent=2))
        print(Fore.GREEN + f'[Spawning-Thread/{_SUCCESS}] Index file write complete / 索引文件写入完成')

        shutil.rmtree(cache_path)
        print(Fore.GREEN + f"[Spawning-Thread/{_SUCCESS}] Write data file complete | 写入数据文件完成")
        return 0
    except FileNotFoundError as e:
        print(Fore.RED + f"[Spawning-Thread/{_ERROR}] {e.filename}：Not Found | 未找到")
        return -1


if __name__ == '__main__':
    spawn_recipes_file(input('Input Minecraft client(server) ".jar" file/path >>>'))

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
