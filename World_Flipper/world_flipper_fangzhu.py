from world_flipper_actions import *
import eventlet
eventlet.monkey_patch()

# 选boss建房之后开始，房主退出再重建
def wf_owner(player,loop_time = 0,count = 0, event_mode = 0):
    if event_mode:
        print("[info] 活动模式，使用设备{0}开始建{1}房...".format(player.use_device,event_screenshot))
    else:
        print("[info] 日常模式，使用设备{0}开始建{1}房...".format(player.use_device,raid_choose))
    if check_game(player): # 从房间内等人开始执行
        while count < loop_time or loop_time == 0:
            with eventlet.Timeout(timeout,False):
                timeout_flag = wait_in_room(player)
                if not timeout_flag: 
                    quit_battle(player)
                    build_from_multiplayer(player)
                else: # 房间没人来，自动解散
                    build_from_multiplayer(player)
                count += 1
                print("{1} [info] 房主已执行{0}次".format(count, Timer().simple_time()))
                continue
            print("超过{0}秒未执行下一次...即将重启游戏...".format(timeout))
            return count

    else: # 从启动游戏开始执行
        with eventlet.Timeout(600,False):
            login(player)
            player.touch((465,809)) # 领主战
            if not event_mode: # 日常模式
                player.wait_touch(raid_choose)
                time.sleep(2)
                player.touch((366,348)) # 选第一个难度
            else: # 活动模式
                time.sleep(3)
                player.wait_touch("button_event") # 活动
                while not player.find("button_duorenyouxi"):
                    player.find_touch(event_screenshot)
                    player.find_touch("button_ok")
            build_from_multiplayer(player,change_zhaomu=True)
        while count < loop_time or loop_time == 0:
            with eventlet.Timeout(timeout,False):
                timeout_flag = wait_in_room(player)
                if not timeout_flag: 
                    quit_battle(player)
                    build_from_multiplayer(player)
                else: # 房间没人来，自动解散
                    build_from_multiplayer(player)
                count += 1
                print("{1} [info] 房主已执行{0}次".format(count, Timer().simple_time()))
                continue
            print("超过{0}秒未执行下一次...即将重启游戏...".format(timeout))
            return count
            
    
if __name__=="__main__":
    player = Autoplayer(use_device=fangzhu_device, adb_path=adb_path,apk_name=wf_apk_name,active_class_name=wf_active_class_name)
    count = 0
    while True:
        # restart_time = Timer().time_restart(datetime.datetime.now())
        count = wf_owner(player,count=count,event_mode=event_mode)
        player.stop_app()
        time.sleep(3)