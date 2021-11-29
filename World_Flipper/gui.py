import sys
import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from typing import Text

sys.path.append("./utils/")
sys.path.append("./")

import eventlet
from settings import *

from world_flipper_actions import *
from world_flipper_fangzhu import *
eventlet.monkey_patch()

class AutoPlayer_WF(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Auto Player WORLD FLIPPER")
        self.geometry("300x300")

        self.notebook = Notebook(self)

        config_tab = tk.Frame(self.notebook)
        fangzhu_tab = tk.Frame(self.notebook)
        canzhan1_tab = tk.Frame(self.notebook)
        canzhan2_tab = tk.Frame(self.notebook)

        # 全局设置
        self.debug_label = tk.Label(config_tab, text="Debug设置").grid(row=0, column=0)
        self.acc_label = tk.Label(config_tab, text="图片匹配精度").grid(row=1, column=0)
        self.wanted_path_label = tk.Label(config_tab, text="目标图片地址").grid(
            row=2, column=0
        )
        self.device_w_label = tk.Label(config_tab, text="设备宽").grid(row=3, column=0)
        self.device_h_label = tk.Label(config_tab, text="设备高").grid(row=4, column=0)
        self.screenshot_blank_label = tk.Label(config_tab, text="截图间隔").grid(
            row=5, column=0
        )
        self.adb_path_label = tk.Label(config_tab, text="ADB路径").grid(row=6, column=0)

        self.debug_entry = tk.Entry(config_tab, bg="white", fg="black")
        self.debug_entry.grid(row=0, column=1)
        self.debug_entry.insert(0, debug)

        self.acc_entry = tk.Entry(config_tab, bg="white", fg="black")
        self.acc_entry.grid(row=1, column=1)
        self.acc_entry.insert(0, accuracy)

        self.wanted_path_entry = tk.Entry(config_tab, bg="white", fg="black")
        self.wanted_path_entry.grid(row=2, column=1)
        self.wanted_path_entry.insert(0, wanted_path)

        self.device_w_entry = tk.Entry(config_tab, bg="white", fg="black")
        self.device_w_entry.grid(row=3, column=1)
        self.device_w_entry.insert(0, device_w)

        self.device_h_entry = tk.Entry(config_tab, bg="white", fg="black")
        self.device_h_entry.grid(row=4, column=1)
        self.device_h_entry.insert(0, device_h)

        self.screenshot_blank_entry = tk.Entry(config_tab, bg="white", fg="black")
        self.screenshot_blank_entry.grid(row=5, column=1)
        self.screenshot_blank_entry.insert(0, screenshot_blank)

        self.adb_path_entry = tk.Entry(config_tab, bg="white", fg="black")
        self.adb_path_entry.grid(row=6, column=1)
        self.adb_path_entry.insert(0, adb_path)

        self.save_button = tk.Button(config_tab, text="保存", command=self.save_config)
        self.save_button.grid(row=7)

        # 房主1
        self.fangzhu_button = tk.Button(fangzhu_tab,text='建房',command=self.fangzhu).pack(fill=tk.X,expand=1)
        
        self.notebook.add(config_tab, text="全局设置")
        self.notebook.add(fangzhu_tab, text="房主")
        self.notebook.add(canzhan1_tab, text="参战1")
        self.notebook.add(canzhan2_tab, text="参战2")

        self.notebook.pack(fill=tk.BOTH, expand=1)

    def init_config(self):
        pass

    def save_config(self, target_language="it", text=None):
        pass
    
    def fangzhu(self):
        player = Autoplayer(use_device=fangzhu_device, adb_path=adb_path,apk_name=wf_apk_name,active_class_name=wf_active_class_name)
        count = 0
        while True:
            restart_time = Timer().time_restart(datetime.datetime.now())
            count = wf_owner(player,count=count,event_mode=event_mode)
            player.stop_app()
            time.sleep(3)


if __name__ == "__main__":
    AutoPlayer_wf = AutoPlayer_WF()
    AutoPlayer_wf.mainloop()
