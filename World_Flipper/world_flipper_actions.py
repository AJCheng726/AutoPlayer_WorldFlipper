import sys
import time
import eventlet

sys.path.append("./utils/")
sys.path.append("./")

import configparser

from utils.Autoplayer import Autoplayer
from utils.Timer import Timer
from utils.print_color import *

config = configparser.ConfigParser()
config.read("./config.ini")

device_w = config["GENERAL"].getint("device_w")
device_h = config["GENERAL"].getint("device_h")
limit_player = config["WF"].getint("limit_player")
battle_timeout = config["WF"].getint("battle_timeout")
fangzhu_account = config["WF"]["fangzhu_account"].split(",")


def check_game(player):
    printWhite("{0} {1} 检查wf是否启动...".format(Timer().simple_time(), player.use_device))
    if player.check_app():
        printWhite("{0} {1} 游戏已启动".format(Timer().simple_time(), player.use_device))
        return 1
    else:
        printWhite("{0} {1} 游戏未启动...".format(Timer().simple_time(), player.use_device))
        return 0


def restart_game(player):
    printWhite("{0} {1} 重启游戏...".format(Timer().simple_time(), player.use_device))
    if player.check_app():
        printWhite("{0} {1} 游戏已启动".format(Timer().simple_time(), player.use_device))
        player.stop_app()
        time.sleep(3)
        player.start_app()
    else:
        printWhite("{0} {1} 游戏未启动...".format(Timer().simple_time(), player.use_device))
        player.start_app()
    return


def check_ui(player):
    if player.debug == 1:
        printWhite("{0} {1} 检查当前所在页面...".format(Timer().simple_time(), player.use_device))
    ui_pages = [
        "button_caidan",
        "button_gonggao",
        "button_gengxinliebiao",
        "page_huodong",
        "button_duorenyouxi",
        "button_duihuandaoju",
        "button_zhaomu",
        "button_pause",
    ]  # 注意顺序，可能同时包含多个特征
    flag = player.find_any(ui_pages)

    if flag == -1:
        if player.debug == 1:
            printWhite("没有找到任何特征，无法确定当前所在页面...")
        return -1
    elif flag == 0:
        if player.debug == 1:
            printWhite("[0]当前处于登录界面")
        return 0
    elif flag == 1:
        if player.debug == 1:
            printWhite("[1]当前处于主城")
        return 1
    elif flag == 2:
        if player.debug == 1:
            printWhite("[2]发现更新列表按钮，当前处于领主战或共斗活动页面")
        return 2
    elif flag == 3:
        if player.debug == 1:
            printWhite("[3]发现小黑对话，当前处于活动页面")
        return 3
    elif flag == 4:
        if player.debug == 1:
            printWhite("[4]发现多人游戏，当前处于建房选择页面")
        return 4
    elif flag == 5:
        if player.debug == 1:
            printWhite("[5]发现兑换道具按钮，当前处于选择难度页面")
        return 5
    elif flag == 6:
        if player.debug == 1:
            printWhite("[6]发现招募按钮，当前处于房间内页面")
        return 6
    elif flag == 7:
        if player.debug == 1:
            printWhite("[7]发现暂停按钮，当前处于战斗中")
        return 7


def login(player):
    printWhite("{0} {1} 自动登录游戏...".format(Timer().simple_time(), player.use_device))
    player.start_app()
    if player.wait_list(["icon_aldlgin", "tips_huanyinghuilai", "button_zhangmidenglu"], max_wait_time=180) != None:  # 自动登录超时为3分钟
        if player.find("button_zhangmidenglu"):
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

    else:
        printWhite("{0} {1} 登录失败，等待重试...".format(Timer().simple_time(), player.use_device))


def goto_main(player):
    printWhite("{0} {1} 前往主城...".format(Timer().simple_time(), player.use_device))
    flag = check_ui(player)
    if flag == 1:
        if player.debug == 1:
            printWhite("[goto_main] 已处于主城")
        return
    elif flag == 6:
        if player.debug == 1:
            printWhite("[goto_main] 处于房间内，放弃任务...")
        player.find_touch("button_fanhui")
        player.wait_touch("button_jiesan", max_wait_time=2)
        time.sleep(2)
        player.touch([135, 919])
    elif player.find("button_jixu"):
        if player.debug == 1:
            printWhite("[goto_main] 处于战斗结束，结算...")
        player.wait_touch("button_jixu", max_wait_time=5)
        player.wait_touch("button_ok(small)", max_wait_time=10)
        time.sleep(5)
        player.touch([135, 919])
    else:
        if player.debug == 1:
            printWhite("[goto_main] 尝试前往主城...")
        player.touch([135, 919])
        time.sleep(2)
        player.touch([135, 919])

    # 检查是否前往成功
    if player.wait("button_gonggao", max_wait_time=5):
        if player.debug == 1:
            printWhite("[goto_main] 已处于主城")
        return
    else:
        if player.debug == 1:
            printWhite("[goto_main] 前往失败,重启游戏...")
        restart_game(player)
        login(player)
        if check_ui(player) == 1:
            if player.debug == 1:
                printWhite("[goto_main] 已处于主城")
            return
        else:
            raise Exception("[goto_main] 跳转主城失败，截图并汇报开发者此错误")


def find_raid(player, raid_choose, raid_rank=1, enter_boss_raid=1):
    printWhite("{0} {1} 寻找raid:{2}".format(Timer().simple_time(), player.use_device, raid_choose))
    if enter_boss_raid == 1:
        player.wait("button_gengxinliebiao")  # 确认进入raid选择界面
    time.sleep(2)
    while not player.wait(raid_choose, 5):
        player.down_swipe()
    player.wait_touch(raid_choose, 0.85)
    rank_pos = [None, (366, 350), (366, 450), (366, 560), (366, 670), (366, 780)]
    time.sleep(2)
    if raid_rank > 0:
        player.touch(rank_pos[raid_rank])  # 按难度点击相应位置


def build_from_multiplayer(player, allow_stranger=False, changeteam=""):
    # 多人游戏→招募→（换队）
    printWhite("{0} {1} 房主建房...".format(Timer().simple_time(), player.use_device))
    # player.wait_touch("button_duorenyouxi", max_wait_time=30)
    player.wait_touch("button_duorenyouxi")
    player.wait_touch("button_shi", max_wait_time=5)

    # 开始招募
    player.wait_touch("button_zhaomu", max_wait_time=60)
    player.wait("icon_zhaomufangshi", max_wait_time=10)
    time.sleep(1)
    danxiang_flag = player.find_any(["button_danxiang0", "button_danxiang1"])
    suiji_flag = player.find_any(["button_suiji0", "button_suiji1"])
    if player.debug == 1:
        printRed(
            "[招募方式识别] danxiang_flag {0}, suiji_flag {1}, allow_stranger {2}".format(danxiang_flag, suiji_flag, allow_stranger)
        )
    if (danxiang_flag == 0 and allow_stranger) or (danxiang_flag == 1 and not allow_stranger):
        player.touch((74, 472))
        time.sleep(1)
    if (suiji_flag == 0 and allow_stranger) or (suiji_flag == 1 and not allow_stranger):
        player.touch((71, 566))
        time.sleep(1)
    player.wait_touch("button_kaishizhaomu", max_wait_time=5)
    
    # 换队
    if changeteam != "":
        change_team(player, team=changeteam)


def wait_in_room(player):
    # 发现战斗中的button_pause返回0，解散返回1
    printWhite("{0} {1} 在房间中等待队友...".format(Timer().simple_time(), player.use_device))
    while not player.find("button_pause"):
        if not (limit_player == 3 and player.find("box_pipeizhong")):
            player.find_touch("button_tiaozhan")
        # if player.find("button_duorenyouxi") or player.find_touch("button_ok"):  # 房间解散
        if player.find_any(["button_duorenyouxi","tips_fangjianjiesan"]) > -1:
            printWhite("{0} {1} 房间解散...准备重建...".format(Timer().simple_time(), player.use_device))
            player.find_touch("button_ok(small)")
            if player.wait("button_pause", max_wait_time = 5):
                quit_battle(player)
            return 1
    return 0


def quit_battle(player):
    printWhite("{0} {1} 房主退出战斗中...".format(Timer().simple_time(), player.use_device))

    # 优化了卡顿时退房
    try:
        with eventlet.Timeout(120, True):
            player.wait("button_pause")
            player.touch_with_checkpoint("button_pause", checkpoint_end="button_fangqi", sleeptime=0.1)
            player.wait_touch("button_fangqi")
            player.wait_touch("button_shi")
            player.wait("button_duorenyouxi")
            return True
    except eventlet.timeout.Timeout:
        printWhite("120秒没退出战斗，应为误结算...结算后重建房...")
        if player.find("button_duorenyouxi"):
            return False
        clear(player)
        return False


def clear(player):
    # 成功结算：等待“继续”→继续→继续→继续→离开房间/OK
    # 结算失败：退出
    printWhite("{0} {1} 等待战斗结算...".format(Timer().simple_time(), player.use_device))
    if player.wait_list(["button_jixu", "G", "button_xuzhan"], max_wait_time=battle_timeout) == "button_jixu":
        player.wait_touch("button_jixu", max_wait_time = 10)
        time.sleep(2)
        while not player.wait_touch("button_jixu", max_wait_time = 5):
            player.touch((device_w * 1 / 2, device_h * 1 / 2))
        time.sleep(2)
        while not player.wait_touch("button_jixu", max_wait_time = 5):
            player.touch((device_w * 1 / 2, device_h * 1 / 2))
            player.wait_touch("button_ok", max_wait_time = 5)
        player.wait_touch_list(["button_likaifangjian","button_jiesan","button_ok"], max_wait_time = 10)
        # while not player.find("icon_fangjianhaoinput"):
        #     player.touch((device_w * 1 / 2, device_h * 1 / 2))
        #     player.find_touch("button_ok")
        #     player.find_touch("button_likaifangjian")
        #     player.find_touch("button_jixu")
        return True
    else:
        player.find_touch("button_ok(small)")  # 发现续战或超过battle_timeout秒，可能阵亡未结算
        return False



def find_room(player, event_mode=0, changeteam=""):
    # 找建房号ID=>"ok"和"是"处理双倍\房满的问题=>没找到就更新=>准备完毕
    printWhite("{0} {1} 再次寻找房间...".format(Timer().simple_time(), player.use_device))
    player.wait("icon_fangjianhaoinput", max_wait_time=10)
    while not player.find("button_zhunbeiwanbi"):
        # player.wait("icon_fangjianhaoinput", max_wait_time=10)
        if event_mode == 1:
            pts = player.find_location("icon_fangjianhaoinput")
            if pts and (pts[0][1] / device_h) > (730 / 960):  # 列表太靠下，没有显示房间
                player.down_swipe()
                time.sleep(2)
        fangzhu = player.find_any(fangzhu_account)
        if fangzhu > -1:
            player.find_touch(fangzhu_account[fangzhu])
        player.wait_touch("button_shi", max_wait_time=2)
        player.wait_touch("button_ok", max_wait_time=2)
        player.find_touch("button_gengxinliebiao")
        # time.sleep(1)
    if changeteam != "":
        change_team(player, changeteam)
    player.wait_touch("button_zhunbeiwanbi", max_wait_time=5, delay=2)


def wait_ring(player, raid):
    # 等要打的铃铛
    printWhite("{0} {1} 等{2}铃铛...".format(Timer().simple_time(), player.use_device, raid))
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


def change_team(player, team=''):
    if team == '': # 如果送来的队伍为空，则不切换队伍
        return -1
    printWhite("{0} {1} 切换队伍至{2}...".format(Timer().simple_time(), player.use_device, team))
    int_team = int(team[2:])
    player.wait_touch("button_biandui", max_wait_time=5)
    player.wait_touch("button_teamset", max_wait_time=10)
    player.wait("label_setbianji")
    player.touch((90 * int(team[0]) - 40, 175))  # 选择set
    time.sleep(3)
    if 10 >= int_team >= 7:
        for i in range(4):
            player.down_swipe(x_start=270, y_start=800, x_end=270, y_end=100)
            time.sleep(1)
        time.sleep(2)
        player.touch((270, 285 + 170 * (int_team - 7)))
    elif 6 >= int_team >= 5:
        player.touch((270, 285 + 170 * 3))
        player.wait("button_teamset", max_wait_time=10)
        for i in range(int_team-4):
            player.swipe((500,320),(40,320))
            time.sleep(1)
    elif 4 >= int_team >= 1:
        player.touch((270, 285 + 170 * (int_team - 1)))
    time.sleep(3)
    player.wait_touch("button_ok2", max_wait_time=5)
    return 0


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("./config.ini")

    player = Autoplayer(
        # use_device=config["WF"]["fangzhu_device"],
        use_device="emulator-5556",
        adb_path=config["GENERAL"]["adb_path"],
        apk_name=config["WF"]["wf_apk_name"],
        active_class_name=config["WF"]["wf_active_class_name"],
        debug=1,
        accuracy=config["GENERAL"].getfloat("accuracy"),
        screenshot_blank=config["GENERAL"].getfloat("screenshot_blank"),
        wanted_path=config["GENERAL"]["wanted_path"],
    )

    # 调试招募方式变更
    # danxiang_flag = player.find_any(["button_danxiang0", "button_danxiang1"])
    # suiji_flag = player.find_any(["button_suiji0", "button_suiji1"])
    # allow_stranger = 0
    # if (danxiang_flag == 0 and allow_stranger) or (danxiang_flag == 1 and not allow_stranger):
    #     player.touch((74, 472))
    #     time.sleep(1)
    # if (suiji_flag == 0 and allow_stranger) or (suiji_flag == 1 and not allow_stranger):
    #     player.touch((71, 566))
    #     time.sleep(1)

    # clear(player)
    player.wait_touch("button_fangqi2", max_wait_time=3)