from nonebot import on_command, Bot
from nonebot.adapters import MessageSegment
from nonebot.adapters.cqhttp import Message, Event, bot as b
from nonebot.rule import to_me

from .GenshinImpactTools.run_api import traveler_passport, GenshinServer

tp = on_command("tp", priority=1)


@tp.handle()
async def handle_first_receive(bot: b.Bot, event: Event, state):
    global server, arg_list
    raw_args = str(event.get_message()).strip()
    if raw_args:
        arg_list = raw_args.split()
    if arg_list[0] == "auto":
        if len(arg_list) <= 1:
            await tp.finish("你好像没有输入UID呀[]~(￣▽￣)~*")
            return
        try:
            int(arg_list[1])
        except ValueError:
            await tp.finish("你输入的根本就不是UID啊啊啊啊")
        if len(arg_list[1]) != 9:
            await tp.finish("你的UID难道不是9位数的？φ(゜▽゜*)♪")
        if int(arg_list[1][0]) not in [1, 5, 6, 7, 8, 9]:
            await tp.finish("你的UID好像不对啊（不存在该服务器）")
    await tp.send("请稍等正在生成中")
    await tp.send(event.get_session_id())
    await tp.send(str(event.get_session_id().split('_')))
    await tp.send(str(bot.get_group_member_info(group_id=int(event.get_session_id().split('_')[1]),
                                                user_id=int(event.get_session_id().split('_')[2]))))

    param = {
        "uid": int(arg_list[1]),
        "name": Message(f"/get_group_member_info,group_id={event.get_session_id().strip('_')[1]},"
                        f"user_id={event.get_session_id().strip('_')[2]}")
    }
    # if int(state["args"][1]) == 1:
    #     server = GenshinServer.Official
    # elif int(state["args"][1]) == 2:
    #     server = GenshinServer.Bilibili
    # elif int(state["args"][1]) == 3:
    #     server = GenshinServer.America
    # elif int(state["args"][1]) == 4:
    #     server = GenshinServer.Europe
    # elif int(state["args"][1]) == 5:
    #     server = GenshinServer.Asia
    # elif int(state["args"][1]) == 6:
    #     server = GenshinServer.HK_MO_TW
    # await tp.send(Message(f'[CQ:image,file=base64://{traveler_passport()}'))
