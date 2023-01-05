# GenshinImpactTools

[![PyPI](https://img.shields.io/pypi/v/GenshinImpactTools)]("https://pypi.org/project/GenshinImpactTools/")
![GitHub last commit](https://img.shields.io/github/last-commit/MingxuanGame/GenshinImpactTools)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/MingxuanGame/GenshinImpactTools/Upload%20to%20PyPI)](https://github.com/MingxuanGame/GenshinImpactTools/actions/workflows/job.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/MingxuanGame/GenshinImpactTools)](https://github.com/MingxuanGame/GenshinImpactTools/releases)
[![GitHub](https://img.shields.io/github/license/MingxuanGame/GenshinImpactTools)](https://github.com/MingxuanGame/GenshinImpactTools/blob/master/LICENSE)
![GitHub all releases](https://img.shields.io/github/downloads/MingxuanGame/GenshinImpactTools/total)
![GitHub Repo stars](https://img.shields.io/github/stars/MingxuanGame/GenshinImpactTools)

[简体中文](docs/README_CN.md)

---

Genshin Impact Tools

Some APIs are built-in (genshin.pub——Traveler's passport，ys.minigg.cn——Inquiry of dishonest personnel, black technology
toolbox，Minigg API)

Deployment method
---

#### 1. Install Python

(This program is written based on **Python 3.9**, **please keep the same version, at least use Python 3.7 or above**)

#### 2. Installation dependencies

You can install dependencies with the following command

```shell
pip install -r requirements.txt
```

#### 3. Install gadgets

Install through the following command

```shell
python setup.py install
```

#### 4. Deploy the browser driver (optional, deploy this step if you need to use the "genshin.pub——Traveler's passport" function)

Install the browser (recommended [Chrome](https://www.google.cn/chrome/index.html)
, [FireFox](https://www.firefox.com.cn), etc.)

Install the driver corresponding to the browser version (Chrome
is [Chrome Driver]([chromedriver.storage.googleapis.com/index.html](http://chromedriver.storage.googleapis.com/index.html))
, FireFox is [Gecko Driver](https://github.com/mozilla/geckodriver/releases) )

Put the driver in the browser installation directory

Built-in API
---

Note: The following functions are all in [run_api.py](GenshinImpactTools/run_api.py)

| Function name                              | Description                 |
| ----------------------------------- | -------------------- |
| [minigg_api_get()](#f1)              | Minigg API call       |
| [traveler_passport()](#f2)                 | genshin.pub——Traveler's passport |
| [untrustworthy_personnel_inquiries()](#f3) | Untrustworthy personnel inquiries         |
| [tools_get()](#f4)                         | Obtaining the Black Technology Toolbox     |

#### <span id="f1">minigg_api_get()</span>

Parameters:

entry: required, type dict, the format is as follows

```
{
    "version":1,    # Version: 0 old version 1 new version
    "type": 0,      # Type: 0 character 1 weapon (used in the new version)
    "char": {       # Role (used in the new version, cannot be queried with weapons at the same time, only the type above is 0 to query)
        "name": [char],         Name (English)
        "talents": 1,           Talent (cannot be queried at the same time as the life seat)
        "constellations": 1     Life seat (cannot be queried with talent at the same time)
    },
    "weapon": [weapon],    Weapon (used in the new version, the English name of the weapon, can only be queried if the above type is 1, and cannot be queried at the same time as the character)
    "data": [entry]    Query data (used in the old version, Chinese name)
}
```

Replace the above "[char]", "[weapon]" and "[entry]" with the content to be queried

Return: the content returned by Minigg API

#### <span id="f2">traveler_passport()</span>

Parameters:

uid：Required, type int, player UID

name：Required, type str, player name

server：Required, type [GenshinServer](GenshinImpactTools/run_api.py), player server

world_level：Required, type int, the world level

save_file：Required, type str, the name of the picture (path)

online_time：Optional, type str, online time

way：Optional, type str, contact information

message：Optional, type str, "What else do you want to say?"

characters：Optional, type set, commonly used roles, the format is as follows

```
{
    ([char], [level], [constellation]),   # char: role name, level: level (not greater than 90, less than 1), constellation: life seat (not greater than 6, less than 0)
    ([char], [level], [constellation]),
    ...
}
```

Replace the above "[char]", "[level]" and "[constellation]" with what you need

Note: The set of this parameter contains at **most four tuples**, otherwise an error will be reported

icon：Optional, type str, avatar (role name)

Throws:

ElementError: Commonly used character avatar elements are wrong

OutOfSpecificationError: Commonly used role level life seat exceeds the specified error

CharacterNameError: Wrong role name

#### <span id="f3">untrustworthy_personnel_inquiries()</span>

Parameters:

account：Required, type str, account of the person being queried

way：Required, type [UntrustworthyPersonnelInquiriesWay](GenshinImpactTools/run_api.py), contact information

bot_name：Optional, type str, robot name

bot_passwd：Optional, type str, robot key

is_transfer_api：Optional, type bool, whether it is an API call (if it is False, it is terminal output)

The bot name and bot passwd in the parameters can use the built-in ones, or use your own

Return:

A dict, the format is as follows

```
{
	'success': True,	# status
	'message': '查询成功',	# message
	'data': {	# data
		'api_0002': {	# API call interface
			'msg': '测试用户111',	# information
			'imgpath': 'https://vkceyugu.cdn.bspapp.com/VKCEYUGU-b3e62dd1-a692-49ac-8be1-67fc7db35559/be5efaa8-8a8b-4c02-be6a-deaa4c8042f1.jpg',	# Evidence screenshot
			'blackcount': 5		# Number of dislikes
		}
	}
}
```

#### <span id="f4">tools_get()</span>

Parameters: none

Return:

A list, the format is as follows

```
[
	{
		'name': '(推荐)原神自动拾取 全分辨率版', 	# Tool name
		'update': '2021-04-29 11:12:45', 	# Update time
		'download': 48, 	# Download times
		'icon': 'https://vkceyugu.cdn.bspapp.com/VKCEYUGU-b3e62dd1-a692-49ac-8be1-67fc7db35559/b63ca2b7-441d-4519-bb83-66d902c97c0a.png', 	# icon
		'description': '适用于所有分辨率的PC端自动拾取工具', 	# briefIntroduction
		'teaching': '运行前提：请以管理员身份运行 执行exe文件……',	# tutorials 
		'video': 'https://vkceyugu.cdn.bspapp.com/VKCEYUGU-b3e62dd1-a692-49ac-8be1-67fc7db35559/3c9ea2b4-b16f-454e-a8a6-42ea1392459f.gif', 	# 演示视频
		'lang': 'AutoHotKey',	# Writing language 
		'author': '喵之召唤师', 	# author
		'download_url': [
		'https://vkceyugu.cdn.bspapp.com/VKCEYUGU-b3e62dd1-a692-49ac-8be1-67fc7db35559/925ed4cc-e254-4676-884a-e031f74b1fd2.zip'
		]	# Download link
	}
	...
]
```

