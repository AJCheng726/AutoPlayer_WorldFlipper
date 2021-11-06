

# 代码示例：
import auto_player as player
import time
from settings import *

loop_time = 0  # 循环次数，若0则无限
count = 0
use_device = main_device

player.adb_test()
print("使用设备：",use_device)
# 大号开始战斗后运行
while(count < loop_time or loop_time == 0):
    player.wait("button_jixu", device=use_device, max_wait_time=600)
    while not player.find("button_likaifangjian", device=use_device):
        player.find_touch("button_jixu", device=use_device)
        player.touch((device_w*1/2,device_h*1/2),device=use_device)

    player.wait_touch("button_likaifangjian", device=use_device, max_wait_time=10)
    while not player.find("button_zhunbeiwanbi", device=use_device):
        player.find_touch("button_gengxinliebiao", device=use_device)
        time.sleep(1)
        player.wait_touch(sub_account, device=use_device,max_wait_time=1)
        player.find_touch("button_shi", device=use_device)
        player.find_touch("button_ok", device=use_device)
    player.wait_touch("button_zhunbeiwanbi", device=use_device, max_wait_time=600)
    count += 1
    print('[info] 农号已执行{0}次'.format(count))