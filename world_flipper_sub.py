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
    # 等待战斗中的暂停键,没出现就一直点挑战
    while not player.find("button_pause", device=use_device):
        player.wait_touch("button_tiaozhan", device=use_device,max_wait_time=5)
    # 没有退出房间之前,无限尝试暂停=>放弃=>"是"
    while not player.find("button_duorenyouxi", device=use_device):
        player.wait_touch("button_pause",  device=use_device,max_wait_time=1)
        player.wait_touch("button_fangqi", device=use_device,max_wait_time=1)
        player.wait_touch("button_shi", device=use_device,max_wait_time=1)
    player.wait_touch("button_duorenyouxi", device=use_device,max_wait_time=60)
    player.wait_touch("button_shi", device=use_device, max_wait_time=5)
    player.wait_touch("button_zhaomu", device=use_device, max_wait_time=60)
    player.wait_touch("button_kaishizhaomu", device=use_device, max_wait_time=5)
    count += 1
    print('[info] 建房号已执行{0}次'.format(count))
