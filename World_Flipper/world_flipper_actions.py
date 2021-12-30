import datetime
import sys
import time

sys.path.append("./utils/")
sys.path.append("./")

import configparser

# from settings import *
from utils.Autoplayer import Autoplayer
from utils.Timer import Timer

config = configparser.ConfigParser()
config.read("./config.ini")

device_w = config["GENERAL"].getint("device_w")
device_h = config["GENERAL"].getint("device_h")
limit_player = config["WF"].getint("limit_player")
battle_timeout = config["WF"].getint("battle_timeout")
fangzhu_account = config["WF"]["fangzhu_account"].split(",")


def check_game(player):
    print(Timer().simple_time(), player.use_device, "检查wf是否启动...")
    if player.check_app():
        print("游戏已启动")
        return 1
    else:
        print("游戏未启动...")
        return 0


def restart_game(player):
    print(Timer().simple_time(), player.use_device, "重启游戏...")
    if player.check_app():
        print("游戏已启动")
        player.stop_app()
        time.sleep(3)
        player.start_app()
    else:
        print("游戏未启动...")
        player.start_app()
    return


def check_ui(player):
    print(Timer().simple_time(), player.use_device, "检查当前所在页面...")
    ui_pages = [
        "button_caidan",
        "button_gonggao",
        "button_gengxinliebiao",
        "page_huodong",
        "button_duorenyouxi",
        "button_duihuandaoju",
    ]
    flag = player.find_any(ui_pages)

    if flag == -1:
        print("没有找到任何特征，无法确定当前所在页面...")
        return -1
    elif flag == 0:
        print("[0]当前处于登录界面")
        return 0
    elif flag == 1:
        print("[1]当前处于主城")
        return 1
    elif flag == 2:
        print("[2]发现更新列表按钮，当前处于领主战或共斗活动页面")
        return 2
    elif flag == 3:
        print("[3]发现小黑对话，当前处于活动页面")
        return 3
    elif flag == 4:
        print("[4]发现多人游戏，当前处于建房选择页面")
        return 4
    elif flag == 5:
        print("[5]发现兑换道具按钮，当前处于选择难度页面")
        return 5


def login(player):
    print(Timer().simple_time(), player.use_device,"自动登录游戏...")
    player.start_app()
    if player.wait("button_zhangmidenglu", max_wait_time=30):  # 需要输账号
        player.find_touch("button_zhangmidenglu")
        time.sleep(1)
        player.touch((441, 486))  # 下拉
        time.sleep(1)
        player.touch((257, 561))  # 选第一个账号
        player.wait_touch("button_denglu")
    while not player.find("page_main"):
        player.find_touch("button_ok")
        player.find_touch("button_fangqi2")
        player.find_touch("button_guanbi")
        player.find_touch("tips_denglujiangli")
        player.touch((device_w * 1 / 2, device_h * 1 / 4))


def goto_main(player):
    print(Timer().simple_time(), player.use_device,"前往主城...")
    flag = check_ui(player)
    if flag == 1:
        print("已处于主城")
    else:
        print("尝试跳转到主城...")
        player.touch([135, 919])
        if player.wait("button_gonggao", max_wait_time=5):
            print("已处于主城")
        else:
            print("前往失败,重启游戏...")
            restart_game(player)
            login(player)
            if check_ui(player) == 1:
                print("已处于主城")
            else:
                raise Exception("跳转主城失败，截图并汇报开发者此错误")


def find_raid(player, raid_choose, difficult=0):
    print(Timer().simple_time(), player.use_device, "寻找raid:" + raid_choose)
    not_in_view = ["raid_fire", "raid_wind"]  # 所选本不在第一页，需要下滑找
    player.wait("button_gengxinliebiao")  # 确认进入raid选择界面
    if raid_choose in not_in_view:
        while not player.wait(raid_choose, 3):
            player.down_swipe()
    player.wait_touch(raid_choose)
    if difficult == 0:
        time.sleep(2)
        player.touch((366, 348))  # 选第一个难度


def build_from_multiplayer(player, change_zhaomu=False):
    print(Timer().simple_time(), player.use_device, "房主建房...")
    player.wait_touch("button_duorenyouxi", max_wait_time=30)
    player.wait_touch("button_shi", max_wait_time=5)
    player.wait_touch("button_zhaomu", max_wait_time=60)
    if change_zhaomu:  # 如果不是互关招募
        time.sleep(1)
        player.touch((74, 472))
        time.sleep(0.5)
        player.touch((71, 566))
    player.wait_touch("button_kaishizhaomu", max_wait_time=5)


def wait_in_room(player):
    print(Timer().simple_time(), player.use_device, "在房间中等待队友...")
    timeout_flag = 0
    while not player.find("button_pause"):
        if not (limit_player == 3 and player.find("box_pipeizhong")):
            player.find_touch("button_tiaozhan")
        if player.find("button_duorenyouxi") or player.find_touch("button_ok"):  # 房间解散
            print(Timer().simple_time(), player.use_device, "房间解散...准备重建...")
            timeout_flag = 1
            break
    return timeout_flag


def quit_battle(player):
    print(Timer().simple_time(), player.use_device, "房主退出战斗中...")
    timer = Timer()
    while not player.find("button_duorenyouxi"):
        player.wait_touch("button_pause", max_wait_time=1)
        player.wait_touch("button_fangqi", max_wait_time=1)
        player.wait_touch("button_shi", max_wait_time=1)
        if timer.get_duration() > 120:
            print("120秒没发现[多人游戏]，应为误结算...结算后重建房...")
            player.wait_touch("button_jixu")
            player.wait_touch("button_jixu")
            return False
    return True


def clear(player):
    # 战斗中=>继续（同时处理升级、掉落）=>离开房间
    print(Timer().simple_time(), player.use_device, "等待战斗结算...")
    if player.wait("button_jixu", max_wait_time=battle_timeout):
        while not player.find("button_likaifangjian"):
            if not player.find_touch("button_jixu"):
                player.touch((device_w * 1 / 2, device_h * 1 / 2))
        player.wait_touch("button_likaifangjian", max_wait_time=10)
    else:
        print("超过{0}秒，可能阵亡未结算...".format(battle_timeout))
        player.find_touch("button_ok")


def find_room(player):
    # 找建房号ID=>"ok"和"是"处理双倍\房满的问题=>没找到就更新=>准备完毕
    print(Timer().simple_time(), player.use_device, "再次寻找房间...")
    while not player.find_touch("button_zhunbeiwanbi"):
        player.find_touch("button_gengxinliebiao")
        time.sleep(1)
        fangzhu = player.find_any(fangzhu_account)
        if fangzhu > -1:
            player.find_touch(fangzhu_account[fangzhu])
        player.find_touch("button_shi")
        player.find_touch("button_ok")


def wait_ring(player, raid):
    # 等要打的铃铛
    print(Timer().simple_time(), player.use_device, "等{0}铃铛...".format(raid))
    while not player.find("button_canjia"):
        player.find_touch("button_lingdang")
    if player.wait(raid, max_wait_time=5):
        player.find_touch("button_canjia")
    else:  # 铃铛不是要打的boss
        player.find_touch("button_bucanjia")
        return 0
    if player.wait_touch("button_zhunbeiwanbi", max_wait_time=5):
        return 1
    else:
        player.find_touch("button_ok")
        return 0


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("./config.ini")

    player = Autoplayer(
        use_device=config["WF"]["fangzhu_device"],
        adb_path=config["GENERAL"]["adb_path"],
        apk_name=config["WF"]["wf_apk_name"],
        active_class_name=config["WF"]["wf_active_class_name"],
        debug=config["GENERAL"].getint("Debug"),
        accuracy=config["GENERAL"].getfloat("accuracy"),
        screenshot_blank=config["GENERAL"].getfloat("screenshot_blank"),
        wanted_path=config["GENERAL"]["wanted_path"],
    )

    player.screen_shot()
    # check_ui(player)
    goto_main(player)
