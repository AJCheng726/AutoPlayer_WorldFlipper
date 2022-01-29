from world_flipper_eventbonus import *

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("./config.ini")

    bonus_device = config["WF"]["loop_device_2"]
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
