import configparser

import eventlet

from world_flipper_actions import *

eventlet.monkey_patch()


def wf_join(player, loop_time=0, count=0, event_mode=0):
    print("[wf_join] 使用设备{0}农BOSS, 搜索房主{1}".format(player.use_device, fangzhu_account))
    if check_game(player):  # 从战斗中开始执行
        while count < loop_time or loop_time == 0:
            with eventlet.Timeout(timeout, False):  # timeout秒还没执行下一次就重启
                clear(player)
                find_room(player)
                count += 1
                print("{1} [info] 农号已执行{0}次".format(count, Timer().simple_time()))
                continue
            print("超过{0}秒未执行下一次...即将重启游戏...".format(timeout))
            return count
    else:  # 从游戏启动开始执行
        with eventlet.Timeout(timeout, False):
            login(player)
            player.touch((465, 809))  # 领主战
            if event_mode:
                time.sleep(3)
                player.wait_touch("button_event")  # 活动
            find_room(player)
        while count < loop_time or loop_time == 0:
            with eventlet.Timeout(timeout, False):
                clear(player)
                find_room(player)
                count += 1
                print("{1} [info] 农号已执行{0}次".format(count, Timer().simple_time()))
                continue
            print("超过{0}秒未执行下一次...即将重启游戏...".format(timeout))
            return count
    return count


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("./config.ini")
    event_screenshot = config["RAID"]["event_screenshot"]
    raid_choose = config["RAID"]["raid_choose"]
    timeout = config["WF"].getint("timeout")
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
        # restart_time = Timer().time_restart(datetime.datetime.now())
        count = wf_join(
            player, count=count, event_mode=config["RAID"].getint("event_mode")
        )
        player.stop_app()
        time.sleep(3)
