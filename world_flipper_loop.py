import auto_player as player
import time
from settings import *

loop_time = 0  # 循环次数，若0则无限
count = 0
use_device = loop_device

player.adb_test()

while(count < loop_time or loop_time == 0):
    player.wait("button_jixu", device=use_device, max_wait_time=600)
    while not player.find("button_zaicitiaozhan", device=use_device):
        player.find_touch("button_jixu", device=use_device)
        player.touch((device_w*1/2,device_h*1/2),device=use_device)
    player.wait_touch("button_zaicitiaozhan",device=use_device,max_wait_time=5)
    player.wait_touch("button_tiaozhan",device=use_device,max_wait_time=10)

    count += 1
    print('[info] 打本已执行{0}次'.format(count))