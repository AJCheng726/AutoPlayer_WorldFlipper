from ast import Raise
from world_flipper_actions import *
from world_flipper_fangzhu import *
from world_flipper_canzhan1 import *
from world_flipper_dailytask import *
from threading import Thread
import configparser
import eventlet

eventlet.monkey_patch()


def double_daily(player1, player2, config, teamconfig):
    daily_maze_choise = config["RAID"]["daily_maze_choise"]
    daily_maze_times = config["RAID"].getint("daily_maze_times")
    daily_hell_choise = config["RAID"]["daily_hell_choise"]
    daily_hell_times = config["RAID"].getint("daily_hell_times")
    daily_raid_times = config["RAID"].getint("daily_raid_times")
    daily_deep_choise = config["RAID"]["daily_deep_choise"]
    daily_deep_times = config["RAID"].getint("daily_deep_times")
    maze_team = teamconfig["MAZE"][daily_maze_choise]
    deep_team = teamconfig["DEEP"][daily_deep_choise]
    hell_team = teamconfig["HELL"][daily_hell_choise]

    daily_announce(player1.use_device, daily_maze_times, daily_hell_times, daily_raid_times, daily_deep_times)
    daily_announce(player2.use_device, daily_maze_times, daily_hell_times, daily_raid_times, daily_deep_times)
    threads1 = [Thread(target=login, args=(player1,)), Thread(target=login, args=(player2,))]
    threads2 = [Thread(target=buy_zhenqipin, args=(player1,)), Thread(target=buy_zhenqipin, args=(player2,))]
    threads3 = [
        Thread(target=maze_repeat, args=(player1, daily_maze_choise, daily_maze_times, maze_team)),
        Thread(target=maze_repeat, args=(player2, daily_maze_choise, daily_maze_times, maze_team)),
    ]
    threads4 = [
        Thread(target=hell_repeat, args=(player1, daily_hell_choise, daily_hell_times, hell_team)),
        Thread(target=hell_repeat, args=(player2, daily_hell_choise, daily_hell_times, hell_team)),
    ]
    threads5 = [
        Thread(target=deep_repeat, args=(player1, daily_deep_choise, daily_deep_times, deep_team)),
        Thread(target=deep_repeat, args=(player2, daily_deep_choise, daily_deep_times, deep_team)),
    ]
    threads6 = [Thread(target=goto_main, args=(player1,)), Thread(target=goto_main, args=(player2,))]

    for t in threads1:
        t.start()
    for t in threads1:
        t.join()
    for t in threads2:
        t.start()
    for t in threads2:
        t.join()
    for t in threads3:
        t.start()
    for t in threads3:
        t.join()
    for t in threads4:
        t.start()
    for t in threads4:
        t.join()
    for t in threads5:
        t.start()
    for t in threads5:
        t.join()
    for t in threads6:
        t.start()
    for t in threads6:
        t.join()

    printBlue("{0} 完成每日任务，返回主城".format(player1.use_device))
    printBlue("{0} 完成每日任务，返回主城".format(player2.use_device))


def double_raid(player1, player2, config, count=5):
    # 交换完成count次共斗
    event_screenshot = config["RAID"]["event_screenshot"]
    raid_choose = config["RAID"]["raid_choose"]
    battle_timeout = config["WF"].getint("battle_timeout")
    event_mode = config["RAID"].getint("event_mode")

    team = teamset_from_ini(
        teamconfig=teamconfig, event_mode=event_mode, raid_choose=raid_choose, event_screenshot=event_screenshot
    )

    threads1 = [
        Thread(target=wf_owner, args=(player1, config, teamconfig, count, 0)),
        Thread(target=wf_join, args=(player2, config, teamconfig, count, 0, battle_timeout)),
    ]
    threads2 = [
        Thread(target=loop_end, args=(player1, config, True)),
        Thread(target=from_prepare_to_main, args=(player2,)),
    ]
    threads3 = [
        Thread(target=wf_owner, args=(player2, config, teamconfig, count, 0)),
        Thread(target=wf_join, args=(player1, config, teamconfig, count, 0, battle_timeout)),
    ]
    threads4 = [
        Thread(target=loop_end, args=(player2, config, True)),
        Thread(target=from_prepare_to_main, args=(player1,)),
    ]

    for t in threads1:
        t.start()
    for t in threads1:
        t.join()
    for t in threads2:
        t.start()
    for t in threads2:
        t.join()
    for t in threads3:
        t.start()
    for t in threads3:
        t.join()
    for t in threads4:
        t.start()
    for t in threads4:
        t.join()


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("./config.ini")

    teamconfig = configparser.ConfigParser()
    teamconfig.read("./teamset.ini")

    devices_list = list(set([config["WF"]["canzhan_device_1"], config["WF"]["canzhan_device_2"], config["WF"]["fangzhu_device"]]))
    if len(devices_list) > 2:
        print("当房主设备与参战1或参战2设备相同时才能正常使用此功能，目前发现设备{0}".format(devices_list))
    player1 = Autoplayer(
        use_device=devices_list[0],
        adb_path=config["GENERAL"]["adb_path"],
        apk_name=config["WF"]["wf_apk_name"],
        active_class_name=config["WF"]["wf_active_class_name"],
        debug=config["GENERAL"].getint("Debug"),
        accuracy=config["GENERAL"].getfloat("accuracy"),
        screenshot_blank=config["GENERAL"].getfloat("screenshot_blank"),
        wanted_path=config["GENERAL"]["wanted_path"],
    )
    player2 = Autoplayer(
        use_device=devices_list[1],
        adb_path=config["GENERAL"]["adb_path"],
        apk_name=config["WF"]["wf_apk_name"],
        active_class_name=config["WF"]["wf_active_class_name"],
        debug=config["GENERAL"].getint("Debug"),
        accuracy=config["GENERAL"].getfloat("accuracy"),
        screenshot_blank=config["GENERAL"].getfloat("screenshot_blank"),
        wanted_path=config["GENERAL"]["wanted_path"],
    )

    double_daily(player1, player2, config, teamconfig)
    double_raid_count = 5
    printBlue("{0} 开始执行互建共斗{1}次".format(devices_list, double_raid_count))
    double_raid(player1, player2, config, double_raid_count)
