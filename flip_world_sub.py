

# 代码示例：
import auto_player as player
import time

loop_time = 0  # 循环次数，若0则无限
count = 1
wait_in_battle = 20
use_device = 'emulator-5554'

player.adb_test()

# 选boss建房之后开始，小号退出再重建
while(count < loop_time or loop_time == 0):
    player.wait_touch("button_tiaozhan", device=use_device, max_wait_time=600)
    time.sleep(wait_in_battle)
    player.wait_touch("button_pause",  device=use_device, max_wait_time=60)
    player.wait_touch("button_fangqi", device=use_device, max_wait_time=5)
    player.wait_touch("button_shi", device=use_device, max_wait_time=5)
    player.wait_touch("button_duorenyouxi", device=use_device,max_wait_time=60)
    player.wait_touch("button_shi", device=use_device, max_wait_time=5)
    player.wait_touch("button_zhaomu", device=use_device, max_wait_time=60)
    player.wait_touch("button_kaishizhaomu", device=use_device, max_wait_time=5)
    count += 1