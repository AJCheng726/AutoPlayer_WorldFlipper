import sys
from world_flipper_actions import *
import configparser

def getbonus(player, loop_time=0):
    printDarkPink("{0} {1} 抽无限池".format(Timer().simple_time(), player.use_device))
    count = 0
    while count < loop_time or loop_time == 0:
        while not player.find_touch("button_chongzhi"):
            player.find_touch("button_chouqu")
        player.wait_touch("button_ok")
        player.wait_touch("button_ok")
        count += 1
        printDarkPink("{0} {1} 抽完{2}轮".format(Timer().simple_time(), player.use_device,count))


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("./config.ini")

    bonus_device = sys.argv[1]
    adb_path = config["GENERAL"]["adb_path"]
    wf_apk_name = config["WF"]["wf_apk_name"]
    wf_active_class_name = config["WF"]["wf_active_class_name"]
    
    player = Autoplayer(
        use_device=bonus_device,
        adb_path=adb_path,
        apk_name=wf_apk_name,
        active_class_name=wf_active_class_name,
    )
    getbonus(player)
