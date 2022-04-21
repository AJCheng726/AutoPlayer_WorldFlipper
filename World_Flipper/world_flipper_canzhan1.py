import configparser
import eventlet
from world_flipper_actions import *

eventlet.monkey_patch()


def from_battle_to_prepare(player, count, event_mode):
    result = clear(player)
    if result:
        find_room(player, event_mode)
        count += 1
        printGreen("{1} {2} 参战已执行{0}次".format(count, Timer().simple_time(), player.use_device))
        return count
    else:
        printRed("{1} {2} 结算失败，寻找房间...".format(count, Timer().simple_time(), player.use_device))
        find_room(player, event_mode)
        return count


def from_main_to_room(player, event_mode, team=""):
    player.touch((465, 809))  # 领主战
    if event_mode:
        time.sleep(3)
        player.wait_touch("button_event")  # 活动
    find_room(player, event_mode, team)


def wf_join(player, loop_time=0, count=0, event_mode=0, timeout=600, battle_timeout=420, team=""):
    printGreen("{0}参战, 搜索{1}，编队{2}".format(player.use_device, fangzhu_account, team))
    if team == "":
        printRed("未在teamset.ini中配置编队，使用默认编队")
    if check_game(player):  # 从战斗中开始执行
        try:
            with eventlet.Timeout(timeout, True):
                if check_ui(player) < 6:  # 处于房间外
                    goto_main(player)
                    from_main_to_room(player, event_mode, team)
        except eventlet.timeout.Timeout:
            printRed("{1} {2} {0}流程超时，即将重启游戏...".format(timeout, Timer().simple_time(), player.use_device))
            return count
        while count < loop_time or loop_time == 0:
            with eventlet.Timeout(battle_timeout, False):  # battle_timeout秒还没执行下一次就重启
                count = from_battle_to_prepare(player, count, event_mode)
                continue
            printRed("{1} {2} {0}战斗超时，即将重启游戏...".format(battle_timeout, Timer().simple_time(), player.use_device))
            return count

    else:  # 从游戏启动开始执行
        try:
            with eventlet.Timeout(timeout, True):
                login(player)
                from_main_to_room(player, event_mode, team)
        except eventlet.timeout.Timeout:
            printRed("{1} {2} {0}流程超时，即将重启游戏...".format(timeout, Timer().simple_time(), player.use_device))
            return count

        while count < loop_time or loop_time == 0:
            with eventlet.Timeout(battle_timeout, False):
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
    event_mode=config["RAID"].getint("event_mode")
    if not event_mode:  # 根据是否活动模式，选择队伍
        team = teamconfig["RAID"][raid_choose]
    else:
        team = teamconfig["RAID"][event_screenshot]
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
            event_mode=config["RAID"].getint("event_mode"),
            timeout=config["WF"].getint("timeout"),
            battle_timeout=battle_timeout,
            team=team,
        )
        player.stop_app()
        time.sleep(3)
