from world_flipper_actions import *
import eventlet
import configparser

eventlet.monkey_patch()


def announcement(event_mode, event_screenshot, raid_choose, player, raid_rank, team, limit_player):
    if event_mode:
        printSkyBlue("活动模式，{0}建{1}房，编队{2}，人数限制{3}...".format(player.use_device, event_screenshot, team, limit_player))
    else:
        printSkyBlue("日常模式，{0}建{1}({2}难度)，编队{3}，人数限制{4}...".format(player.use_device, raid_choose, raid_rank, team, limit_player))


def one_loop(player, count, limit_player, allow_stranger=False, quit=True):
    # 在房间等待→结算→建房→开始招募
    timeout_flag = wait_in_room(player, limit_player=limit_player)
    if quit == True:  # 灵车
        if not timeout_flag:
            quit_battle(player)
            build_from_multiplayer(player, allow_stranger=allow_stranger)
        else:  # 房间没人来，自动解散
            build_from_multiplayer(player, allow_stranger=allow_stranger)
    else:  # 正常结算
        if not timeout_flag:
            clear(player)
            build_from_multiplayer(player, allow_stranger=allow_stranger)
        else:  # 房间没人来，自动解散
            build_from_multiplayer(player, allow_stranger=allow_stranger)
    count += 1
    printSkyBlue("{1} {2} 房主已执行{0}次".format(count, Timer().simple_time(), player.use_device))
    return count


def from_main_to_room(event_mode, raid_choose, event_screenshot, allow_stranger, player, raid_rank, changeteam):
    # 主页→建房间→开始招募
    player.touch((465, 809))  # 领主战
    if not event_mode:  # 日常模式
        find_raid(player, raid_choose, raid_rank=raid_rank)
    else:  # 活动模式
        player.wait('button_gengxinliebiao')
        time.sleep(1)
        player.touch([88,242]) # 活动
        # time.sleep(3)
        # player.wait_touch("button_event")  # 活动
        while not player.find("button_duorenyouxi"):
            find_raid(player, event_screenshot, raid_rank=0)
            player.find_touch("button_ok")
    build_from_multiplayer(player, allow_stranger=allow_stranger, changeteam=changeteam)
    printSkyBlue("{1} {2} 房主已执行{0}次".format(1, Timer().simple_time(), player.use_device))


def wf_owner(player, config, teamconfig, event_mode, loop_time=0, count=0):
    # 选boss建房之后开始，房主退出再重建
    announcement(event_mode, event_screenshot, raid_choose, player, raid_rank, team, limit_player)
    if not check_game(player):  # 游戏未启动
        try:
            with eventlet.Timeout(timeout, True):
                login(player)
        except eventlet.timeout.Timeout:
            printSkyBlue("{1} {2} {0}秒游戏未登录，重启...".format(timeout, Timer().simple_time(), player.use_device))
            return count
    # 进游戏→主城→找raid→建房→招募→战斗
    try:
        with eventlet.Timeout(timeout, True):
            goto_main(player)
            from_main_to_room(event_mode, raid_choose, event_screenshot, allow_stranger, player, raid_rank, changeteam=team)
            count += 1
    except eventlet.timeout.Timeout:
        printSkyBlue("{1} {2} {0}秒未第一次挑战，重启游戏...".format(timeout, Timer().simple_time(), player.use_device))
        return count
    # 循环
    while count < loop_time or loop_time == 0:
        with eventlet.Timeout(timeout, False):
            count = one_loop(player, count, limit_player=limit_player, allow_stranger=allow_stranger, quit=True)
            continue
        printSkyBlue("{1} {2} {0}秒未开始挑战，重启游戏...".format(timeout, Timer().simple_time(), player.use_device))
        return count
    return count


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("./config.ini")

    teamconfig = configparser.ConfigParser()
    teamconfig.read("./teamset.ini")
    timeout = config["WF"].getint("timeout")
    limit_player = config["WF"].getint("limit_player")
    allow_stranger = config["WF"].getint("allow_stranger")

    event_screenshot = config["RAID"]["event_screenshot"]
    raid_choose = config["RAID"]["raid_choose"]
    raid_rank = config["RAID"].getint("raid_rank")
    event_mode = config["RAID"].getint("event_mode")

    team = teamset_from_ini(
        teamconfig=teamconfig, event_mode=event_mode, raid_choose=raid_choose, event_screenshot=event_screenshot
    )

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
        count = wf_owner(player, config, teamconfig, count=count, event_mode=event_mode)
        player.stop_app()
        time.sleep(3)
