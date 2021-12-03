from world_flipper_actions import *
import eventlet
import configparser

eventlet.monkey_patch()

# 选boss建房之后开始，房主退出再重建
def wf_ring(player, config, loop_time=0, count=0):
    timeout = config["WF"].getint("timeout")
    raid = config["RAID"]["ring_raid_choose"]

    print("[info] 使用设备{0}开始执行蹭铃铛...".format(player.use_device))
    if check_game(player):  # 从房间内等人开始执行
        while count < loop_time or loop_time == 0:
            with eventlet.Timeout(timeout, False):
                ring_flag = 0
                while ring_flag == 0:
                    ring_flag = wait_ring(player, raid)
                clear(player)
                count += 1
                print("{1} [info] {2} 蹭铃铛已执行{0}次".format(count, Timer().simple_time(), player.use_device))
                continue
            print("超过{0}秒未执行下一次...即将重启游戏...".format(timeout))
            return count

    else:  # 从启动游戏开始执行
        with eventlet.Timeout(600, False):
            login(player)
        while count < loop_time or loop_time == 0:
            with eventlet.Timeout(timeout, False):
                ring_flag = 0
                while ring_flag == 0:
                    ring_flag = wait_ring(player, raid)
                clear(player)
                count += 1
                print("{1} [info] {2} 蹭铃铛已执行{0}次".format(count, Timer().simple_time(), player.use_device))
                continue
            print("超过{0}秒未执行下一次...即将重启游戏...".format(timeout))
            return count


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("./config.ini")

    player = Autoplayer(
        use_device=config["WF"]["ring_device"],
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
        count = wf_ring(player, config, count=count)
        player.stop_app()
        time.sleep(3)
