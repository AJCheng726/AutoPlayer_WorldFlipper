from cv2 import repeat
from world_flipper_actions import *
from world_flipper_fangzhu import *
import configparser
import eventlet

eventlet.monkey_patch()


def daily_announce(daily_maze_times, daily_hell_times, daily_raid_times, daily_deep_times):
    total_ap = daily_maze_times * 14 + daily_hell_times * 30 + daily_raid_times * 18 + daily_deep_times * 20
    printDarkBlue(
        "{0} 开始每日任务，打{1}次迷宫、{2}次地狱、{3}次深层、{4}次共斗，预计消耗{5}体力，需要提前嗑药".format(
            player.use_device, daily_maze_times, daily_hell_times, daily_deep_times, daily_raid_times, total_ap
        )
    )


def buy_zhenqipin(player, items_count=8):
    printBlue("{0} 清空商店，购买{1}个珍奇品".format(player.use_device, items_count))
    goto_main(player)
    player.touch([315, 916])  # 前往商店页面
    player.wait_touch("icon_zhenqipin", delay=1)
    player.wait("tips_zhenqipin")
    for i in range(items_count):
        try:
            with eventlet.Timeout(10, True):
                print("{0} 购买第{1}个珍品".format(player.use_device, i+1))
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
    if repeat == 0:
        return
    printBlue("{0} 开始每日任务，打{1}次{2},编队{3}".format(player.use_device, repeat, maze_choise, maze_team))
    goto_main(player)
    player.touch([93, 842])
    # player.wait_touch(maze_choise)
    find_raid(player, maze_choise, raid_rank=1, enter_boss_raid=0)
    # player.wait("button_wanfajieshao")
    # player.touch([261, 349])
    player.wait_touch("button_shi", max_wait_time=5)
    if maze_team != "":
        change_team(player, maze_team)
    for i in range(repeat - 1):
        player.wait_touch("button_tiaozhan")
        player.wait_touch("button_jixu")
        player.wait_touch("button_zaicitiaozhan")
        printBlue("{0} 完成了{2}次{1}".format(player.use_device, maze_choise, i + 1))
    player.wait_touch("button_tiaozhan")
    player.wait_touch("button_jixu")
    player.wait_touch("button_ok(small)")
    printBlue("{0} 完成了{2}次{1}".format(player.use_device, maze_choise, repeat))
    player.wait("page_main", max_wait_time=5)


def hell_repeat(player, hell_choise, repeat=2):
    if repeat == 0:
        return
    printBlue("{0} 地狱本，打{1}次{2},编队{3}".format(player.use_device, repeat, hell_choise, hell_team))
    goto_main(player)
    player.touch([93, 842])
    player.wait_touch("hell_enter")
    find_raid(player, hell_choise, raid_rank=0, enter_boss_raid=0)
    player.wait_touch("diff_hell")
    player.wait_touch("button_shi", max_wait_time=5)
    if hell_team != "":
        change_team(player, hell_team)
    player.wait_touch("button_tiaozhan")
    i = 0
    while i < repeat - 1:
        flag = player.wait_list(["button_jixu", "G", "button_xuzhan"])
        if flag == "button_jixu":
            printBlue("{0} 完成了{2}次{1}".format(player.use_device, hell_choise, i + 1))
            player.wait_touch("button_jixu")
            player.wait_touch("button_zaicitiaozhan")
            player.wait_touch("button_tiaozhan")
            i += 1
        elif flag == "G":
            printRed("{0} 地狱本失败,重试".format(player.use_device))
            player.wait_touch("button_fangqi3")
            player.wait_touch("button_ok(small)")
            player.wait_touch("diff_hell")
            player.wait_touch("button_shi", max_wait_time=5)
            player.wait_touch("button_tiaozhan")
    player.wait_touch("button_jixu")
    player.wait_touch("button_ok(small)")
    printBlue("{0} 完成了{2}次{1}".format(player.use_device, hell_choise, repeat))
    player.wait("page_main", max_wait_time=5)
        
        
    player.wait_touch("button_jixu")
    player.wait_touch("button_ok(small)")
    printBlue("{0} 完成了{2}次{1}".format(player.use_device, hell_choise, repeat))
    player.wait("page_main", max_wait_time=5)


def deep_repeat(player, deep_choise, repeat):
    if repeat == 0:
        return
    printBlue("{0} 深层任务，打{1}次{2},编队{3}".format(player.use_device, repeat, deep_choise, deep_team))
    goto_main(player)
    player.touch([93, 842])
    player.wait_touch("deep_enter")
    find_raid(player, deep_choise, raid_rank=0, enter_boss_raid=0)
    if maze_team != "":
        change_team(player, deep_team)
    player.wait_touch("button_tiaozhan")
    for i in range(repeat - 1):
        player.wait_touch("button_jixu")
        player.wait_touch("button_zaicitiaozhan")
        printBlue("{0} 完成了{2}次{1}".format(player.use_device, deep_choise, i + 1))
        player.wait_touch("button_tiaozhan")
    player.wait_touch("button_jixu")
    player.wait_touch("button_ok(small)")
    printBlue("{0} 完成了{2}次{1}".format(player.use_device, deep_choise, repeat))
    player.wait("page_main", max_wait_time=5)


def host_raid(player, repeat=3):
    if repeat == 0:
        return
    printBlue("{0} 完成{1}次每日共斗".format(player.use_device, repeat))
    announcement(event_mode, event_screenshot, raid_choose, player, raid_rank, raid_team, limit_player=3)
    goto_main(player)
    from_main_to_room(
        player=player,
        event_mode=event_mode,
        raid_choose=raid_choose,
        event_screenshot=event_screenshot,
        allow_stranger=True,
        raid_rank=raid_rank,
        changeteam=raid_team,
    )
    count = 1
    for i in range(repeat - 1):
        count = one_loop(player=player, count=count, allow_stranger=True, quit=False, limit_player=3)
    wait_in_room(player, limit_player=3)
    clear(player)
    player.wait("page_main", max_wait_time=5)
    return 0


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("./config.ini")

    teamconfig = configparser.ConfigParser()
    teamconfig.read("./teamset.ini")

    daily_device = config["WF"]["daily_device"]
    daily_maze_choise = config["RAID"]["daily_maze_choise"]
    daily_maze_times = config["RAID"].getint("daily_maze_times")
    daily_hell_choise = config["RAID"]["daily_hell_choise"]
    daily_hell_times = config["RAID"].getint("daily_hell_times")
    daily_raid_choise = config["RAID"]["daily_raid_choise"]
    daily_raid_times = config["RAID"].getint("daily_raid_times")
    daily_deep_choise = config["RAID"]["daily_deep_choise"]
    daily_deep_times = config["RAID"].getint("daily_deep_times")
    adb_path = config["GENERAL"]["adb_path"]
    wf_apk_name = config["WF"]["wf_apk_name"]
    wf_active_class_name = config["WF"]["wf_active_class_name"]
    maze_team = teamconfig["MAZE"][daily_maze_choise]
    deep_team = teamconfig["DEEP"][daily_deep_choise]
    hell_team = teamconfig["HELL"][daily_hell_choise]

    # 每日raid使用房主的参数
    raid_choose = config["RAID"]["raid_choose"]
    event_mode = config["RAID"].getint("event_mode")
    event_screenshot = config["RAID"]["event_screenshot"]
    raid_rank = config["RAID"].getint("raid_rank")
    raid_team = teamset_from_ini(teamconfig, event_mode, raid_choose, event_screenshot)

    player = Autoplayer(
        use_device=daily_device,
        adb_path=adb_path,
        apk_name=wf_apk_name,
        active_class_name=wf_active_class_name,
        debug=config["GENERAL"].getint("Debug"),
    )

    # 开始每日
    daily_announce(daily_maze_times, daily_hell_times, daily_raid_times, daily_deep_times)
    if not check_game(player):
        login(player)
    buy_zhenqipin(player)
    maze_repeat(player, maze_choise=daily_maze_choise, repeat=daily_maze_times)
    hell_repeat(player, hell_choise=daily_hell_choise, repeat=daily_hell_times)
    host_raid(player, repeat=daily_raid_times)
    deep_repeat(player, deep_choise=daily_deep_choise, repeat=daily_deep_times)
    goto_main(player)
    printBlue("{0} 完成每日任务，返回主城".format(player.use_device))
