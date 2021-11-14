from world_flipper_canzhan1 import *
from settings import *

if __name__=='__main__':
    player = Autoplayer(
        use_device=canzhan_device_2,
        adb_path=adb_path,
        apk_name=wf_apk_name,
        active_class_name=wf_active_class_name,
    )
    count = 0
    while True:
        restart_time = Timer().time_restart(datetime.datetime.now())
        count = wf_join(player,count)
        player.stop_app()
        time.sleep(3)