# todo：超时重建
import datetime
import time

import auto_player as player
from settings import *

# 选boss建房之后开始，房主退出再重建
def wf_owner(use_device,loop_time = 0):
    player.adb_test()
    count = 0

    print("[info] 使用设备{0}开始建房...".format(use_device))
    while count < loop_time or loop_time == 0:
        # 等待战斗中的暂停键,没出现就一直点挑战
        timeout_flag = False
        print(datetime.datetime.now(),"(stage1) 在房间中等待队友...")
        while not player.find("button_pause", device=use_device):
            player.find_touch("button_tiaozhan", device=use_device)
            if player.find("button_duorenyouxi", device=use_device) or player.find_touch("button_ok", device=use_device): # 房间解散
                print(datetime.datetime.now(),"房间解散...准备重建...")
                timeout_flag = True
                break

        # 没有退出房间之前,无限尝试暂停=>放弃=>"是"
        if not timeout_flag:
            print(datetime.datetime.now(),"(stage2) 房主退出战斗中...")
            while not player.find("button_duorenyouxi", device=use_device):
                player.wait_touch("button_pause", device=use_device, max_wait_time=1)
                player.wait_touch("button_fangqi", device=use_device, max_wait_time=1)
                player.wait_touch("button_shi", device=use_device, max_wait_time=1)
            if wait_outof_room > 0:
                print("防止等待超时，等待{0}秒后重新建房...".format(wait_outof_room))
                time.sleep(wait_outof_room)

        print(datetime.datetime.now(),"(stage3) 房主重建房...")
        player.wait_touch("button_duorenyouxi", device=use_device, max_wait_time=1)
        player.wait_touch("button_shi", device=use_device, max_wait_time=5)
        player.wait_touch("button_zhaomu", device=use_device, max_wait_time=60)
        player.wait_touch("button_kaishizhaomu", device=use_device, max_wait_time=5)
        count += 1
        print("{1} [info] 房主已执行{0}次".format(count, datetime.datetime.now()))

wf_owner(use_device = fangzhu_device)