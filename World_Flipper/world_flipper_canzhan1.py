from world_flipper_actions import *
import eventlet
eventlet.monkey_patch()

def wf_join(player, loop_time=0, count = 0):
    print("[wf_join] 使用设备{0}农BOSS, 搜索房主{1}".format(player.use_device, fangzhu_account))
    if check_game(player):  # 从战斗中开始执行
        while count < loop_time or loop_time == 0:
            with eventlet.Timeout(600,False): # 600秒还没执行下一次就重启
                clear(player)
                find_room(player)
                count += 1
                print("{1} [info] 农号已执行{0}次".format(count, Timer().simple_time()))
                continue
            print("超过600秒未执行下一次...即将重启游戏...")
            return count
    else:  # 从游戏启动开始执行
        with eventlet.Timeout(timeout,False):
            login(player)
            player.touch((465, 809))  # 领主战
            find_room(player)
            while count < loop_time or loop_time == 0: # 600秒还没执行下一次就重启
                with eventlet.Timeout(600,False):
                    clear(player)
                    find_room(player)
                    count += 1
                    print("{1} [info] 农号已执行{0}次".format(count, Timer().simple_time()))
                    continue
                print("超过600秒未执行下一次...即将重启游戏...")
                return count
    return count


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
        count = wf_join(player,count)
        player.stop_app()
        time.sleep(3)
