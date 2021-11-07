import auto_player as player
import time
from settings import *

loop_time = 0  # 循环次数，若0则无限
count = 0
use_device = main_device

player.adb_test()
print("使用设备：",use_device,"农BOSS, 搜索小号房",sub_account)
while(count < loop_time or loop_time == 0):
    # 战斗中=>继续（同时处理升级、掉落）=>离开房间
    player.wait("button_jixu", device=use_device, max_wait_time=600)
    while not player.find("button_likaifangjian", device=use_device):
        player.find_touch("button_jixu", device=use_device)
        player.touch((device_w*1/2,device_h*1/2),device=use_device)
    player.wait_touch("button_likaifangjian", device=use_device, max_wait_time=10)

    # 找建房号ID=>"ok"和"是"处理双倍\房满的问题=>没找到就更新=>准备完毕
    while not player.find_touch("button_zhunbeiwanbi", device=use_device):
        player.find_touch(sub_account, device=use_device)
        player.find_touch("button_shi", device=use_device)
        player.find_touch("button_ok", device=use_device)
        player.find_touch("button_gengxinliebiao", device=use_device)
    count += 1
    print('[info] 农号已执行{0}次'.format(count))