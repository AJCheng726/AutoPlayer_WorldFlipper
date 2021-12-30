import configparser

import eventlet

from world_flipper_actions import *

eventlet.monkey_patch()

def from_battle_to_prepare(player,count):
    clear(player)
    find_room(player)
    count += 1
    print("{1} [info] {2} 农号已执行{0}次".format(count, Timer().simple_time(), player.use_device))
    return count

def from_main_to_room(player,event_mode):
    player.touch((465, 809))  # 领主战
    if event_mode:
        time.sleep(3)
        player.wait_touch("button_event")  # 活动
    find_room(player)

def wf_join(player, loop_time=0, count=0, event_mode=0, timeout=600):
    print("[wf_join] 使用设备{0}农BOSS, 搜索房主{1}".format(player.use_device, fangzhu_account))
    if check_game(player):  # 从战斗中开始执行
        with eventlet.Timeout(120, False):
            if check_ui(player) < 6: # 处于房间外
                goto_main(player)
                from_main_to_room(player,event_mode)
        while count < loop_time or loop_time == 0:
            with eventlet.Timeout(timeout, False):  # timeout秒还没执行下一次就重启
                count = from_battle_to_prepare(player,count)
                continue
            print("超过{0}秒未执行下一次...即将重启游戏...".format(timeout))
            return count

    else:  # 从游戏启动开始执行
        with eventlet.Timeout(120, False):
            login(player)
            from_main_to_room(player,event_mode)

        while count < loop_time or loop_time == 0:
            with eventlet.Timeout(timeout, False):
                count = from_battle_to_prepare(player,count)
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
            player, count=count, event_mode=config["RAID"].getint("event_mode"), timeout=config["WF"].getint("timeout"),
        )
        player.stop_app()
        time.sleep(3)
