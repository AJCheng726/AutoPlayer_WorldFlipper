from world_flipper_canzhan1 import *
from settings import *

if __name__=='__main__':
    player = Autoplayer(use_device=canzhan_device_2, adb_path=adb_path,apk_name=wf_apk_name,active_class_name=wf_active_class_name)
    wf_join(player)