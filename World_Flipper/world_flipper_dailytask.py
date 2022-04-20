from cv2 import repeat
from world_flipper_actions import *
import configparser
import eventlet

eventlet.monkey_patch()


def buy_zhenqipin(player, items_count=8):
    printBlue("{0} 完成每日任务，清空商店".format(player.use_device))
    goto_main(player)
    player.touch([315, 916])  # 前往商店页面
    player.wait_touch("icon_zhenqipin", delay=1)
    player.wait("tips_zhenqipin")
    for i in range(items_count):
        try:
            with eventlet.Timeout(10, True):
                print("{0} 购买第1个珍品".format(player.use_device))
                player.wait("tips_zhenqipin")
                player.touch([325, 350])
                player.wait("button_goumai")
                player.swipe([340, 530], [400, 530])
                if player.wait_touch("button_goumai", max_wait_time=5):
                    time.sleep(2)
                    continue
                else:
                    continue
        except:
            printBlue("{0} 购买超时，商店已清空".format(player.use_device))
            return


def maze_repeat(player, maze_choise="maze_fire", repeat=4):
    printBlue("{0} 开始每日任务，打{1}次{2}".format(player.use_device, repeat, maze_choise))
    goto_main(player)
    player.touch([93, 842])
    # player.wait_touch(maze_choise)
    find_raid(player, maze_choise, raid_rank=1, enter_boss_raid=0)
    # player.wait("button_wanfajieshao")
    # player.touch([261, 349])
    player.wait_touch("button_shi", max_wait_time=5)
    for i in range(repeat):
        player.wait_touch("button_tiaozhan")
        player.wait_touch("button_jixu")
        player.wait_touch("button_zaicitiaozhan")
        printBlue("{0} 完成了1次{1}".format(player.use_device, maze_choise))
    goto_main(player)


def daily_task(player, maze_choise="maze_fire", repeat=4):
    if not check_game(player):
        login(player)
    buy_zhenqipin(player)
    maze_repeat(player, maze_choise=maze_choise, repeat=repeat)
    printBlue("{0} 完成每日任务，返回主城".format(player.use_device))


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("./config.ini")

    daily_device = config["WF"]["daily_device"]
    maze_choise = config["RAID"]["daily_maze_choise"]
    adb_path = config["GENERAL"]["adb_path"]
    wf_apk_name = config["WF"]["wf_apk_name"]
    wf_active_class_name = config["WF"]["wf_active_class_name"]

    player = Autoplayer(
        use_device=daily_device,
        adb_path=adb_path,
        apk_name=wf_apk_name,
        active_class_name=wf_active_class_name,
    )
    daily_task(player, maze_choise=maze_choise, repeat=4)
