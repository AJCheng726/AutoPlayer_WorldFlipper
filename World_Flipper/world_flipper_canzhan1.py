from world_flipper_actions import *


def wf_join(player, loop_time=0):
    print("[wf_join] 使用设备{0}农BOSS, 搜索房主{1}".format(player.use_device, fangzhu_account))
    if login(player):  # 从战斗中开始执行
        while count < loop_time or loop_time == 0:
            clear(player)
            if player.check_restart(restart_time):  # 重启游戏
                time.sleep(5)
                return
            find_room(player)
            count += 1
            print("{1} [info] 农号已执行{0}次".format(count, datetime.datetime.now()))
    else:  # 从游戏启动开始执行
        player.touch((465, 809))  # 领主战
        find_room(player)
        while count < loop_time or loop_time == 0:
            clear(player)
            find_room(player)
            if player.check_restart(restart_time):  # 重启游戏
                time.sleep(5)
                return
            count += 1
            print("{1} [info] 农号已执行{0}次".format(count, datetime.datetime.now()))


if __name__ == "__main__":
    player = Autoplayer(
        use_device=canzhan_device_1,
        adb_path=adb_path,
        apk_name=wf_apk_name,
        active_class_name=wf_active_class_name,
    )
    count = 0
    while True:
        restart_time = Timer().time_restart(datetime.datetime.now())
        wf_join(player)
