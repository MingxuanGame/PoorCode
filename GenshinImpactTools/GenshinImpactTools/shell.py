from colorama import Style, Fore

from .run_api import untrustworthy_personnel_inquiries, UntrustworthyPersonnelInquiriesWay, tools_get


def shell():
    print(f"\n{'=' * 20}原神小工具{'=' * 20}")
    print("(1)失信人员查询\n"
          "(2)获取黑科技工具箱中的所有工具信息\n")
    option = int(input("请输入命令编号："))
    if option == 1:
        number = input("请输入被查询人员的号码：")
        way = input("请输入联系方式（QQ/微信/交易平台）：")
        while True:
            if way.upper() == "QQ":
                way_enum = UntrustworthyPersonnelInquiriesWay.QQ
                break
            elif way == "微信":
                way_enum = UntrustworthyPersonnelInquiriesWay.Wechat
                break
            elif way == "交易平台":
                way_enum = UntrustworthyPersonnelInquiriesWay.Pay
                break
            else:
                way = input("请重新输入（QQ/微信/交易平台）：")
        untrustworthy_personnel_inquiries(number, way_enum, is_transfer_api=False)
    elif option == 2:
        tools = tools_get()
        print(f"\n{'=' * 20}原神小工具{'=' * 20}")
        for tool in tools:
            print(f"工具名：{tool['name']}\n"
                  f"最后更新时间：{tool['update']}\n"
                  f"下载次数：{tool['download']}\n"
                  f"作者：{tool['author']}\n"
                  f"图标：{tool['icon']}\n"
                  f"演示视频：{tool['video']}\n"
                  f"简介：{tool['description']}\n"
                  f"教程：{tool['teaching']}\n"
                  f"编写语言：{tool['lang']}")
            try:
                print("下载地址：\n{}".format('\n'.join(tool['download_url'])) + f"\n{'=' * 50}")
            except TypeError:
                print("下载地址：无" + f"\n{'=' * 50}")
        print(f"{Fore.YELLOW}注意：工具来源于原神账号管理云平台（https://ys.minigg.cn），请谨防其可能带来的潜在风险。{Style.RESET_ALL}")


if __name__ == '__main__':
    __package__ = "GenshinImpactTools"  # Debug
    shell()
