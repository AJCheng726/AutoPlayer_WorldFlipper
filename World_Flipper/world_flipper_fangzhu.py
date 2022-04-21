from world_flipper_actions import *
import eventlet
import configparser

eventlet.monkey_patch()


def announcement(event_mode, event_screenshot, raid_choose, player, raid_rank, team):
    if event_mode:
        printSkyBlue("活动模式，{0}建{1}房，编队{2}...".format(player.use_device, event_screenshot, team))
    else:
        printSkyBlue("日常模式，{0}建{1}({2}难度)，编队{3}...".format(player.use_device, raid_choose, raid_rank, team))
    if team == "":
        printRed("未在teamset.ini中配置编队，使用默认编队")


def one_loop(player, count, allow_stranger=False):
    timeout_flag = wait_in_room(player)
    if not timeout_flag:
        quit_battle(player)
        build_from_multiplayer(player, allow_stranger=allow_stranger)
    else:  # 房间没人来，自动解散
        build_from_multiplayer(player, allow_stranger=allow_stranger)
    count += 1
    printSkyBlue("{1} {2} 房主已执行{0}次".format(count, Timer().simple_time(), player.use_device))
    return count


def from_main_to_room(event_mode, raid_choose, event_screenshot, allow_stranger, player, raid_rank, changeteam):
    player.touch((465, 809))  # 领主战
    if not event_mode:  # 日常模式
        find_raid(player, raid_choose, raid_rank=raid_rank)
    else:  # 活动模式
        time.sleep(3)
        player.wait_touch("button_event")  # 活动
        while not player.find("button_duorenyouxi"):
            find_raid(player, event_screenshot, raid_rank=0)
            player.find_touch("button_ok")
    build_from_multiplayer(player, allow_stranger=allow_stranger, changeteam=changeteam)


# 选boss建房之后开始，房主退出再重建
def wf_owner(player, config, teamconfig, loop_time=0, count=0, event_mode=0):
    timeout = config["WF"].getint("timeout")
    allow_stranger = config["WF"].getint("allow_stranger")

    event_screenshot = config["RAID"]["event_screenshot"]
    raid_choose = config["RAID"]["raid_choose"]
    raid_rank = config["RAID"].getint("raid_rank")

    if not event_mode:  # 根据是否活动模式，选择队伍
        team = teamconfig["RAID"][raid_choose]
    else:
        team = teamconfig["RAID"][event_screenshot]

    announcement(event_mode, event_screenshot, raid_choose, player, raid_rank, team)

    if check_game(player):  # 游戏已启动
        try:
            with eventlet.Timeout(timeout, True):
                if check_ui(player) < 6:  # 处于房间外
                    goto_main(player)
                    from_main_to_room(
                        event_mode, raid_choose, event_screenshot, allow_stranger, player, raid_rank, changeteam=team
                    )
                    count += 1
                    printSkyBlue("{1} {2} 房主已执行{0}次".format(count, Timer().simple_time(), player.use_device))
        except eventlet.timeout.Timeout:
            printSkyBlue("{1} {2} {0}秒未进入房间，即将重启游戏...".format(timeout, Timer().simple_time(), player.use_device))
            return count
        while count < loop_time or loop_time == 0:
            with eventlet.Timeout(timeout, False):
                count = one_loop(player, count, allow_stranger=allow_stranger)
                continue
            printSkyBlue("{1} {2} {0}秒未执行下一次，即将重启游戏...".format(timeout, Timer().simple_time(), player.use_device))
            return count

    else:  # 从启动游戏开始执行
        try:
            with eventlet.Timeout(timeout, True):
                login(player)
                from_main_to_room(event_mode, raid_choose, event_screenshot, allow_stranger, player, raid_rank, changeteam=team)
                count += 1
                printSkyBlue("{1} {2} 房主已执行{0}次".format(count, Timer().simple_time(), player.use_device))
        except eventlet.timeout.Timeout:
            printSkyBlue("{1} {2} {0}秒未进入房间，即将重启游戏...".format(timeout, Timer().simple_time(), player.use_device))
            return count
        while count < loop_time or loop_time == 0:
            with eventlet.Timeout(timeout, False):
                count = one_loop(player, count, allow_stranger=allow_stranger)
                continue
            printSkyBlue("{1} {2} {0}秒未执行下一次...即将重启游戏...".format(timeout, Timer().simple_time(), player.use_device))
            return count


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("./config.ini")

    teamconfig = configparser.ConfigParser()
    teamconfig.read("./teamset.ini")

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
    count = 0
    while True:
        count = wf_owner(player, config, teamconfig, count=count, event_mode=config["RAID"].getint("event_mode"))
        player.stop_app()
        time.sleep(3)
