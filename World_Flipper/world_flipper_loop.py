from world_flipper_actions import *

def loop(player,loop_time = 0):
    print("使用设备{0}循环打本".format(player.use_device))
    count = 0
    while(count < loop_time or loop_time == 0):
        player.wait("button_jixu", max_wait_time=600)
        while not player.find("button_zaicitiaozhan"):
            player.find_touch("button_jixu")
            player.touch((device_w*1/2,device_h*1/2))
        player.wait_touch("button_zaicitiaozhan",max_wait_time=5)
        while not player.find("button_pause"):
            player.wait_touch("button_tiaozhan",max_wait_time=10)

        count += 1
        print('[info] 打本已执行{0}次'.format(count))

if __name__=='__main__':
    player = Autoplayer(use_device=loop_device, adb_path=adb_path,apk_name=wf_apk_name,active_class_name=wf_active_class_name)
    loop(player)