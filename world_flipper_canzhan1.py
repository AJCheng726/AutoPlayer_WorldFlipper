# todo：阵亡再进
import datetime
import time

import auto_player as player
from settings import *
from utils.Timer import  Timer

def wf_join(use_device,loop_time = 0):
    count = 0
    player.adb_test()
    print("[info] 使用设备{0}农BOSS, 搜索房主{1}".format(use_device, fangzhu_account))
    while count < loop_time or loop_time == 0:
        # 战斗中=>继续（同时处理升级、掉落）=>离开房间
        print(datetime.datetime.now(),"(stage1) 等待战斗结算...")
        if player.wait("button_jixu", device=use_device, max_wait_time=timeout):
            while not player.find("button_likaifangjian", device=use_device):
                player.find_touch("button_jixu", device=use_device)
                player.touch((device_w * 1 / 2, device_h * 1 / 2), device=use_device)
            player.wait_touch("button_likaifangjian", device=use_device, max_wait_time=10)
        else:
            print("超过{0}秒，可能阵亡未结算...".format(timeout))
            player.find_touch("button_ok", device=use_device)

        # 找建房号ID=>"ok"和"是"处理双倍\房满的问题=>没找到就更新=>准备完毕
        print(datetime.datetime.now(),"(stage2) 再次寻找房间...")
        while not player.find_touch("button_zhunbeiwanbi", device=use_device):
            player.find_touch(fangzhu_account, device=use_device)
            player.find_touch("button_shi", device=use_device)
            player.find_touch("button_ok", device=use_device)
            player.find_touch("button_gengxinliebiao", device=use_device)
        count += 1
        print("[info] {1} 农号已执行{0}次".format(count, datetime.datetime.now()))

if __name__=='__main__':
    wf_join(use_device = canzhan_device_1)