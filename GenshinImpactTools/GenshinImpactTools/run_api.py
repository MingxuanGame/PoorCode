import base64
import json
import re
import time
from enum import Enum, unique
from json import JSONDecodeError

import requests
from colorama import Fore, Style
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from .error import SimultaneousQueryError, CharacterNameError, ElementError, OutOfSpecificationError

character_coordinate = {
    "七七": 8,
    "刻晴": 8,
    "达达利亚": 8,
    "可莉": 11,
    "温迪": 8,
    "琴": 9,
    "莫娜": 10,
    "迪卢克": 12,
    "钟离": 8,
    "阿贝多": 10,
    "凝光": 7,
    "北斗": 7,
    "行秋": 7,
    "重云": 7,
    "香菱": 8,
    "丽莎": 9,
    "凯亚": 9,
    "安柏": 9,
    "班尼特": 10,
    "砂糖": 7,
    "芭芭拉": 9,
    "菲谢尔": 10,
    "诺艾尔": 9,
    "迪奥娜": 10,
    "雷泽": 11,
    "辛焱": 7,
    "空": 11,
    "荧": 11,
    "甘雨": 11,
    "魈": 10,
    "胡桃": 13,
    "罗莎莉亚": 12,
    "烟绯": 14,
    "优菈": 13,
}


@unique
class UntrustworthyPersonnelInquiriesWay(Enum):
    QQ = "QQ"
    Wechat = "微信"
    Pay = "交易平台"


@unique
class GenshinServer(Enum):
    Official = "官服 - 天空岛"
    Bilibili = "B服 - 世界树"
    America = "America"
    Europe = "Europe"
    Asia = "Asia"
    HK_MO_TW = "港澳台"


def traveler_passport(uid: int, name: str, server: GenshinServer, world_level: int, save_file: str,
                      online_time: str = "", way: str = "", message: str = "", characters: set = None,
                      icon: str = None, is_base_64 = False) -> None:
    global _character_info, _icon_info
    _driver = _web_driver()
    _driver.maximize_window()
    _driver.get("https://genshin.pub/id_card")
    _driver.find_element_by_css_selector('input[maxlength="9"]').send_keys(uid)
    _driver.find_element_by_css_selector('input[maxlength="14"]').send_keys(name)
    time.sleep(0.2)
    _driver.find_element_by_css_selector('div[style="height: 40px; width: 200px; margin-left: -25px;"]').click()
    _driver.find_element_by_css_selector(f'li[data-value="{server.value}"]').click()
    _driver.find_elements_by_css_selector('div[id="demo-simple-select-outlined"]')[1].click()
    time.sleep(0.2)
    _driver.find_element_by_css_selector(f'li[data-value="{world_level}"]').click()
    for _i, _input_box in enumerate(_driver.find_elements_by_css_selector('input[maxlength="30"]')):
        if _i == 0:
            _input_box.send_keys(online_time)
        elif _i == 1:
            _input_box.send_keys(way)
    _driver.find_element_by_css_selector('textarea').send_keys(message)
    _error = []
    if characters is not None:
        for _i, _character in enumerate(characters):
            try:
                _character_info = json.loads(requests.get(f"https://genshin.minigg.cn/?data={_character[0]}").text[20:])
                _character_element = _character_info["角色信息"]["神之眼"]
                pass
            except JSONDecodeError:
                _error.append(_character[0])
                continue
            except KeyError:
                _character_element = _character_info["角色信息"]["神之心"]
            if _character_element == "无":
                raise ElementError(_character[0])
            _driver.find_element_by_css_selector('img[src="/images/id_card/add.svg"]').click()
            time.sleep(0.1)
            for _box in _driver.find_elements_by_xpath("/html/body/div[2]/div[3]/div/div/div/div")[0:6]:
                if _box.text == _character_element:
                    _box.click()
                    _driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div/div[%i]/div/div/div/p" %
                                                  character_coordinate[_character[0]]).click()
                    _driver.find_element_by_xpath(
                        f"/html/body/div/div/div/div/div[5]/div/div/div[{_i + 7}]/div[3]/div").click()
                    time.sleep(0.2)
                    try:
                        _driver.find_element_by_xpath(f"/html/body/div[2]/div[3]/ul/li[{_character[1]}]").click()
                    except NoSuchElementException:
                        raise OutOfSpecificationError(_character[0], _character[1], False)
                    time.sleep(0.2)
                    _driver.find_element_by_xpath(
                        f"/html/body/div/div/div/div/div[5]/div/div/div[{_i + 7}]/div[5]/div").click()
                    time.sleep(0.2)
                    try:
                        _driver.find_element_by_xpath(f"/html/body/div[2]/div[3]/ul/li[{_character[2] + 1}]").click()
                    except NoSuchElementException:
                        raise OutOfSpecificationError(_character[0], _character[2], True)
                    time.sleep(0.2)
                    break

    if icon is not None:
        _driver.find_element_by_xpath("/html/body/div/div/div/div/div[5]/div/div/div[3]/div[2]/div[2]").click()
        try:
            _icon_info = json.loads(requests.get(f"https://genshin.minigg.cn/?data={icon}").text[20:])
            _icon_element = _icon_info["角色信息"]["神之眼"]
            pass
        except JSONDecodeError:
            raise CharacterNameError([icon])
        except KeyError:
            _icon_element = _icon_info["角色信息"]["神之心"]
        if _icon_element == "无":
            raise ElementError(icon)
        for _box in _driver.find_elements_by_xpath("/html/body/div[2]/div[3]/div/div/div/div")[0:6]:
            if _box.text == _icon_element:
                _box.click()
                _driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div/div[%i]/div/div/div/p" %
                                              character_coordinate[icon]).click()

    _driver.find_element_by_xpath(f"/html/body/div/div/div/div/div[5]/div/div/div[1]/div[2]").click()
    while True:
        if _driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[1]/span").text == "制作成功啦！":
            if is_base_64:
                if len(_error) > 0:
                    raise CharacterNameError(_error)
                del _error
                base = _driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[2]/img").get_attribute("src")
                _driver.quit()
                return re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", base
                                                           , re.DOTALL).groupdict().get("data")
            else:
                with open(save_file, "wb") as f:
                    f.write(base64.urlsafe_b64decode(re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)",
                                                               _driver.find_element_by_xpath(
                                                                   "/html/body/div[2]/div[3]/div/div[2]/img")
                                                               .get_attribute("src"), re.DOTALL).groupdict().get("data")))
            break

    if len(_error) > 0:
        raise CharacterNameError(_error)
    del _error
    _driver.quit()
    pass


def untrustworthy_personnel_inquiries(account: str, way: UntrustworthyPersonnelInquiriesWay,
                                      bot_name: str = "paimonbot",
                                      bot_passwd: str = "J14yjfIXneWyXSo", is_transfer_api: bool = True) \
        -> [str, None]:
    url = "https://b3e62dd1-a692-49ac-8be1-67fc7db35559.bspapp.com/http/genshincloudapi"
    params = {
        "bot_name": bot_name,
        "bot_pass": bot_passwd,
        "api_code": "0002",
        "term_credit": account,
        "term_way": way.value
    }
    get_json = requests.get(url=url, params=params).text
    if is_transfer_api:
        return json.loads(get_json)
    else:
        get_dict = json.loads(get_json)
        print(f"\n{'=' * 20}原神小工具{'=' * 20}")
        if get_dict['success']:
            print("状态：成功")
            print(f"查询的账号：{account}")
            print(f"联系方式：{way.value}")
            if get_dict['data']['api_0002']['msg'] != "此用户暂无失信记录" and \
                    "此用户为信用担保用户" not in get_dict['data']['api_0002']['msg']:
                print(Fore.RED + "发现失信记录，请谨慎交易！")
                print(f"失信原因：{get_dict['data']['api_0002']['msg']}")
                print(f"证据截图：{get_dict['data']['api_0002']['imgpath']}")
                print(f"被踩次数：{get_dict['data']['api_0002']['blackcount']}{Style.RESET_ALL}")
            else:
                print(f"{Fore.LIGHTGREEN_EX}信用信息：{get_dict['data']['api_0002']['msg']}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}注意：数据来源于原神账号管理云平台（https://ys.minigg.cn），仅供参考。举报骗子入口：QQ 2575525962{Style.RESET_ALL}")
        else:
            print("状态：失败")
            try:
                print(f"失败原因：{get_dict['message']}")
            except KeyError:
                print(f"失败原因：" + get_dict['error']['message'].strip('"').strip(':'))
        pass  # breakpoint


def minigg_api_get(entry: dict) -> str:
    url = "https://genshin.minigg.cn"
    return requests.get(url=url, params=_entry_to_get(entry)).text


def _entry_to_get(entry):
    params = {}
    try:
        if entry["version"] == 1:
            # New version
            if entry["type"] == 0:
                char = entry["char"]
                params["char"] = char["name"]
                if "talents" in char.keys() and "constellations" in char.keys():
                    raise SimultaneousQueryError("talents", "constellations")
                elif "talents" in char.keys():
                    params["talents"] = char["talents"]
                elif "constellations" in char.keys():
                    params["constellations"] = char["constellations"]
            elif entry["type"] == 1:
                params["weapon"] = entry["weapon"]
        elif entry["version"] == 0:
            # Old version
            params["data"] = entry["data"]
    except KeyError:
        pass
    return params


def tools_get() -> list:
    params = {
        "bot_name": "paimonbot",
        "bot_pass": "J14yjfIXneWyXSo",
        "api_code": "0008",
    }
    tools_dict = json.loads(requests.get(url="https://b3e62dd1-a692-49ac-8be1-67fc7db35559.bspapp.com/http"
                                             "/genshincloudapi",
                                         params=params).text)
    tools = []
    for tool in tools_dict["data"]["api_0008"]:
        tools.append({
            "name": tool["filetitle"],
            "update": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tool["lastupdate"] / 1000)),
            "download": tool["downloadnum"],
            "icon": tool["isopath"],
            "description": tool["doc"],
            "teaching": tool["doctext"],
            "video": tool["videopath"],
            # "condition": tool[""],
            "lang": tool["createtype"],
            "author": tool["ownernickname"],
            "download_url": tool["filepath"]
        })
    return tools


def _web_driver():
    try:
        # Chrome
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        chrome_options.add_experimental_option('perfLoggingPrefs', {'enableNetwork': True})
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  desired_capabilities=caps)
    except WebDriverException:
        try:
            # FireFox
            driver = webdriver.Firefox()
        except WebDriverException:
            # Edge
            try:
                driver = webdriver.Edge()
            except WebDriverException:
                driver = webdriver.PhantomJS()
    return driver


pass  # breakpoint
