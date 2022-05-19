import configparser
import eventlet
from world_flipper_actions import *

eventlet.monkey_patch()


def from_battle_to_prepare(player, count, event_mode):
    # clear→找房间→准备完毕
    result = clear(player)
    if result:
        find_room(player, event_mode)
        count += 1
        printGreen("{1} {2} 参战已执行{0}次".format(count, Timer().simple_time(), player.use_device))
        return count
    else:
        printRed("{1} {2} 阵亡或解散，寻找房间...".format(count, Timer().simple_time(), player.use_device))
        find_room(player, event_mode)
        return count


def from_main_to_room(player, event_mode, team=""):
    # 主页→领主战→房间→准备完毕
    player.touch((465, 809))  # 领主战
    if event_mode:
        player.wait('button_gengxinliebiao')
        time.sleep(1)
        player.touch([88,242]) # 活动
        # player.wait_touch("button_event")  # 活动
    find_room(player, event_mode, team)


def wf_join(player, event_mode, team, loop_time=0, count=0, timeout=600, battle_timeout=420):
    # （登录）→第一次进房间→循环
    printGreen("{0}参战, 搜索{1}，编队{2}".format(player.use_device, fangzhu_account, team))
    if not check_game(player):  # 游戏未启动
        try:
            with eventlet.Timeout(timeout, True):
                login(player)
        except eventlet.timeout.Timeout:
            printRed("{1} {2} {0}秒未登录，重启游戏...".format(timeout, Timer().simple_time(), player.use_device))
            return count
    # 第一次进房间
    try:
        with eventlet.Timeout(timeout, True):
            goto_main(player)
            from_main_to_room(player, event_mode, team)
            count += 1
            printGreen("{1} {2} 参战已执行{0}次".format(count, Timer().simple_time(), player.use_device))
    except eventlet.timeout.Timeout:
        printRed("{1} {2} {0}秒未第一次参战，重启游戏...".format(timeout, Timer().simple_time(), player.use_device))
        return count
    # 循环
    while count < loop_time or loop_time == 0:
        with eventlet.Timeout(battle_timeout, False):  # battle_timeout秒还没执行下一次就重启
            count = from_battle_to_prepare(player, count, event_mode)
            continue
        printRed("{1} {2} {0}战斗超时，即将重启游戏...".format(battle_timeout, Timer().simple_time(), player.use_device))
        return count
    return count


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("./config.ini")

    teamconfig = configparser.ConfigParser()
    teamconfig.read("./teamset.ini")

    event_screenshot = config["RAID"]["event_screenshot"]
    raid_choose = config["RAID"]["raid_choose"]
    timeout = config["WF"].getint("timeout")
    battle_timeout = config["WF"].getint("battle_timeout")
    event_mode = config["RAID"].getint("event_mode")
    team = teamset_from_ini(
        teamconfig=teamconfig, event_mode=event_mode, raid_choose=raid_choose, event_screenshot=event_screenshot
    )
    player = Autoplayer(
        use_device=config["WF"]["canzhan_device_1"],
        adb_path=config["GENERAL"]["adb_path"],
        apk_name=config["WF"]["wf_apk_name"],
        active_class_name=config["WF"]["wf_active_class_name"],
        debug=config["GENERAL"].getint("Debug"),
        accuracy=config["GENERAL"].getfloat("accuracy"),
        screenshot_blank=config["GENERAL"].getfloat("screenshot_blank"),
        wanted_path=config["GENERAL"]["wanted_path"],
    )
    count = 0
    while True:
        count = wf_join(
            player,
            count=count,
            event_mode=event_mode,
            timeout=timeout,
            battle_timeout=battle_timeout,
            team=team,
        )
        player.stop_app()
        time.sleep(3)
