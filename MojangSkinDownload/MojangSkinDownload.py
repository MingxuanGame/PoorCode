#encoding:utf-8

#获取玩家UUID
name = input('输入Minecraft用户名:')
url1 = 'https://api.mojang.com/users/profiles/minecraft/' + name    #Mojang API（UUID）
from urllib import request
with request.urlopen(url1) as file:
    uuiddata = file.read()
uuiddata = str(uuiddata)     #Byte转String

#计算Base64
jsu = len(name)
print('已经获取玩家UUID，正在获取皮肤Base64')
uuiddata = uuiddata[jsu + 19:-3]      #UUID获取
url2 = 'https://sessionserver.mojang.com/session/minecraft/profile/' + uuiddata   #计算Base64
with request.urlopen(url2) as file:
    skindata = file.read()
skindata = skindata[jsu+123:-9]

#解码Base64
print('已经获取皮肤Base64，正在解码')
import base64
skin = base64.b64decode(skindata).decode()      #解码
skintf = skin[299+jsu:-20]
if skintf != 'slim"':           #判断纤细皮肤
    skin = skin[154+jsu:-13]
else:
    skin = skin[154+jsu:-68]

#下载文件
print("已经获取玩家皮肤下载地址")
import requests
filename = input('输入皮肤文件保存名称，支持中文:')
r = requests.get(skin)
print('正在下载')
with open(filename + ".png",'wb') as f:
    f.write(r.content)
sjdhshdh = input("下载成功，按回车键关闭")