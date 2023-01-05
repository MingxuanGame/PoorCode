# GenshinImpactTools

[![PyPI](https://img.shields.io/pypi/v/GenshinImpactTools)]("https://pypi.org/project/GenshinImpactTools/")
![GitHub last commit](https://img.shields.io/github/last-commit/MingxuanGame/GenshinImpactTools)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/MingxuanGame/GenshinImpactTools/Upload%20to%20PyPI)](https://github.com/MingxuanGame/GenshinImpactTools/actions/workflows/job.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/MingxuanGame/GenshinImpactTools)](https://github.com/MingxuanGame/GenshinImpactTools/releases)
[![GitHub](https://img.shields.io/github/license/MingxuanGame/GenshinImpactTools)](https://github.com/MingxuanGame/GenshinImpactTools/blob/master/LICENSE)
![GitHub all releases](https://img.shields.io/github/downloads/MingxuanGame/GenshinImpactTools/total)
![GitHub Repo stars](https://img.shields.io/github/stars/MingxuanGame/GenshinImpactTools)

[English](../README.md)

---

原神小工具

内置了一些API（可莉特调——旅行者护照，原神账号管理云平台——失信人员查询，黑科技工具箱，Minigg API）

部署方法
---

#### 1.安装Python

（本程序基于**Python 3.9**编写，**请最好保持同版本，至少使用Python 3.7以上版本**）

#### 2.安装依赖

你可以通过如下命令安装依赖

```shell
pip install -r requirements.txt
```

#### 3.安装小工具

通过如下命令安装

```shell
python setup.py install
```

#### 4.部署浏览器驱动（可选，如果需要使用“可莉特调——旅行者护照”功能则部署这一步）

安装浏览器（推荐[Chrome](https://www.google.cn/chrome/index.html) 、[FireFox](https://www.firefox.com.cn/) 等）

安装与浏览器版本对应的驱动（Chrome是[ChromeDriver]([chromedriver.storage.googleapis.com/index.html](http://chromedriver.storage.googleapis.com/index.html))
、FireFox是[GeckoDriver](https://github.com/mozilla/geckodriver/releases) ）

将驱动程序放在浏览器安装目录下

内置API
---

注：以下函数均在[run_api.py](../GenshinImpactTools/run_api.py)

| 函数名                              | 描述                 |
| ----------------------------------- | -------------------- |
| [minigg_api_get()](#f1)              | Minigg API调用       |
| [traveler_passport()](#f2)                 | 可莉特调——旅行者护照 |
| [untrustworthy_personnel_inquiries()](#f3) | 失信人员查询         |
| [tools_get()](#f4)                         | 黑科技工具箱获取     |

#### <span id="f1">minigg_api_get()</span>

参数：

entry：必填，类型dict，格式如下

```
{
    "version":1,    # 版本：0旧版 1新版
    "type": 0,      # 类型：0角色 1武器（用于新版）
    "char": {       # 角色（用于新版，不能和武器同时查询，要上面的type为0才能查询）
        "name": [char],         # 名称（英文）
        "talents": 1,           # 天赋（不能和命座同时查询）
        "constellations": 1     # 命座（不能和天赋同时查询）
    },
    "weapon": [weapon],    # 武器（用于新版，武器英文名，要上面的type为1才能查询，不能和角色同时查询）
    "data": [entry]    # 查询数据（用于旧版，中文名）
}
```

上面的“[char]”，“[weapon]”和“ [entry]”替换为要查询的内容

返回：Minigg API返回的内容

#### <span id="f2">traveler_passport()</span>

参数：

uid：必填，类型int，玩家UID

name：必填，类型str，玩家名称

server：必填，类型[GenshinServer](../GenshinImpactTools/run_api.py) ，玩家服务器

world_level：必填，类型int，世界等级

save_file：必填，类型str，图片保存的名称（路径）

online_time：选填，类型str，在线时间

way：选填，类型str，联系方式

message：选填，类型str，”还有啥别的想说的？“

characters：选填，类型set，常用角色，格式如下

```
{
    ([char], [level], [constellation]),   # char：角色名称，level：等级（不能大于90，小于1），constellation：命座（不能大于6，小于0）
    ([char], [level], [constellation]),
    ...
}
```

上面的“[char]”，“[level]”和“ [constellation]”替换为自己需要的

注：本参数的set内**最多含有四个元组**，否则报错

icon：选填，类型str，头像（角色名）

抛出：

ElementError：常用角色/头像元素错误

OutOfSpecificationError：常用角色等级/命座超出规定错误

CharacterNameError：错误角色名称错误

#### <span id="f3">untrustworthy_personnel_inquiries()</span>

参数：

account：必填，类型str，被查询人的账号

way：必填，类型[UntrustworthyPersonnelInquiriesWay](../GenshinImpactTools/run_api.py) ，联系方式

bot_name：选填，类型str，机器人名称

bot_passwd：选填，类型str，机器人密钥

is_transfer_api：选填，类型bool，是否为API调用（若为False则为终端输出）

参数中的bot_name和bot_passwd可以使用内置的，也可使用自己的

返回：

一个dict，格式如下

```
{
	'success': True,	# 状态
	'message': '查询成功',	# 信息
	'data': {	# 数据
		'api_0002': {	# API调用接口
			'msg': '测试用户111',	# 消息
			'imgpath': 'https://vkceyugu.cdn.bspapp.com/VKCEYUGU-b3e62dd1-a692-49ac-8be1-67fc7db35559/be5efaa8-8a8b-4c02-be6a-deaa4c8042f1.jpg',	# 证据截图
			'blackcount': 5		# 被踩次数
		}
	}
}
```

#### <span id="f4">tools_get()</span>

参数：无

返回：

一个list，格式如下

```
[
	{
		'name': '(推荐)原神自动拾取 全分辨率版', 	# 工具名称
		'update': '2021-04-29 11:12:45', 	# 更新时间
		'download': 48, 	# 下载次数
		'icon': 'https://vkceyugu.cdn.bspapp.com/VKCEYUGU-b3e62dd1-a692-49ac-8be1-67fc7db35559/b63ca2b7-441d-4519-bb83-66d902c97c0a.png', 	# 图标
		'description': '适用于所有分辨率的PC端自动拾取工具', 	# 简介
		'teaching': '运行前提：请以管理员身份运行 执行exe文件……',	# 教程 
		'video': 'https://vkceyugu.cdn.bspapp.com/VKCEYUGU-b3e62dd1-a692-49ac-8be1-67fc7db35559/3c9ea2b4-b16f-454e-a8a6-42ea1392459f.gif', 	# 演示视频
		'lang': 'AutoHotKey',	# 编写语言 
		'author': '喵之召唤师', 	# 作者
		'download_url': [
		'https://vkceyugu.cdn.bspapp.com/VKCEYUGU-b3e62dd1-a692-49ac-8be1-67fc7db35559/925ed4cc-e254-4676-884a-e031f74b1fd2.zip'
		]	# 下载地址
	}
	...
]
```

