

# 代码示例：
import auto_player as player
import time
from settings import *

loop_time = 0  # 循环次数，若0则无限
count = 0
wait_in_battle = 20
use_device = main_device
sleep_in_battle = 5

player.adb_test()

# 大号开始战斗后运行
while(count < loop_time or loop_time == 0):
    while not player.find_touch("button_jixu", device=use_device, tap = False):
        time.sleep(sleep_in_battle)
        player.touch((270,480),device=use_device)
        player.find_touch("button_ok",device=use_device)

    for i in range(4):
        player.wait_touch("button_jixu", device=use_device, max_wait_time=10)
        time.sleep(1)
    player.wait_touch("button_likaifangjian", device=use_device, max_wait_time=30)
    while not player.find_touch("button_zhunbeiwanbi", device=use_device, tap = False):
        player.wait_touch("button_gengxinliebiao", device=use_device, max_wait_time=1)
        player.wait_touch("xiaohaoid", device=use_device, max_wait_time=1)
        player.wait_touch("button_shi", device=use_device, max_wait_time=1)
        # player.wait_touch("button_chufaqian", device=use_device, max_wait_time=1)
        player.wait_touch("button_ok", device=use_device, max_wait_time=1)
    player.wait_touch("button_zhunbeiwanbi", device=use_device, max_wait_time=600)
    count += 1
    print('[info] 农号已执行{0}次'.format(count))