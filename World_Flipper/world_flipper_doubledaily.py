from world_flipper_actions import *
from world_flipper_fangzhu import *
from world_flipper_canzhan1 import *
from threading import Thread
import configparser
import eventlet

eventlet.monkey_patch()


def shuangrengongdou(player1, player2, count=5):
    # 交换完成count次共斗
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

    event_screenshot = config["RAID"]["event_screenshot"]
    raid_choose = config["RAID"]["raid_choose"]
    timeout = config["WF"].getint("timeout")
    battle_timeout = config["WF"].getint("battle_timeout")
    event_mode = config["RAID"].getint("event_mode")
    limit_player = config["WF"].getint("limit_player")
    allow_stranger = config["WF"].getint("allow_stranger")
    raid_rank = config["RAID"].getint("raid_rank")
    event_mode = config["RAID"].getint("event_mode")

    team = teamset_from_ini(
        teamconfig=teamconfig, event_mode=event_mode, raid_choose=raid_choose, event_screenshot=event_screenshot
    )

    devices_list = list(set([config["WF"]["canzhan_device_1"], config["WF"]["canzhan_device_2"], config["WF"]["fangzhu_device"]]))
    count = 2
    printBlue("{0} 开始执行互建共斗{1}次".format(devices_list, count))

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
    shuangrengongdou(player1, player2, count)
