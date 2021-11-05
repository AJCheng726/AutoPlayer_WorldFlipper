import time

import auto_player as player
from settings import *

loop_time = 0  # 循环次数，若0则无限
count = 0
wait_in_battle = 20
wait_out_battle = 30
use_device = sub_device

player.adb_test()

# 选boss建房之后开始，小号退出再重建
while(count < loop_time or loop_time == 0):
    if player.wait("button_tiaozhan", device=use_device, max_wait_time=600):
        player.find_touch("button_tiaozhan", device=use_device)
    else:
        raise Exception("房间自动解散了...")
    while not player.find("button_duorenyouxi", device=use_device):
        player.wait_touch("button_pause",  device=use_device,max_wait_time=1)
        player.wait_touch("button_fangqi", device=use_device,max_wait_time=1)
        time.sleep(1)
        player.wait_touch("button_shi", device=use_device,max_wait_time=1)
    player.wait_touch("button_duorenyouxi", device=use_device,max_wait_time=60)
    player.wait_touch("button_shi", device=use_device, max_wait_time=5)
    player.wait_touch("button_zhaomu", device=use_device, max_wait_time=60)
    player.wait_touch("button_kaishizhaomu", device=use_device, max_wait_time=5)
    count += 1
    print('[info] 建房号已执行{0}次'.format(count))
