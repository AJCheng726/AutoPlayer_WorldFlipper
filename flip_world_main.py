

# 代码示例：
import auto_player as player
import time

loop_time = 0  # 循环次数，若0则无限
count = 0
wait_in_battle = 20
use_device = 'emulator-5556'

player.adb_test()

# 大号开始战斗后运行
while(count < loop_time or loop_time == 0):
    player.wait_touch("button_jixu", device=use_device, max_wait_time=600)
    player.wait_touch("button_jixu", device=use_device, max_wait_time=10)
    player.wait_touch("button_jixu", device=use_device, max_wait_time=10)
    player.wait_touch("button_jixu", device=use_device, max_wait_time=3)
    player.wait_touch("button_likaifangjian", device=use_device, max_wait_time=30)
    while not player.wait_touch("button_zhunbeiwanbi", device=use_device, tap = False):
        player.wait_touch("button_gengxinliebiao", device=use_device, max_wait_time=1)
        # player.wait_touch("xiaohaoid", device=use_device, max_wait_time=1)
        player.wait_touch("button_chufaqian", device=use_device, max_wait_time=1)
    player.wait_touch("button_zhunbeiwanbi", device=use_device, max_wait_time=600)
    count += 1
    print('[info] 已执行{0}次'.format(count))