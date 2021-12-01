import subprocess
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.ttk import Notebook
from typing import Text

sys.path.append("./utils/")
sys.path.append("./")

import configparser

import eventlet

from world_flipper_actions import *
from world_flipper_fangzhu import *

# from settings import *


eventlet.monkey_patch()


class AutoPlayer_WF(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Auto Player WORLD FLIPPER")
        self.geometry("240x350")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
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

        self.debug_entry = tk.Entry(config_tab, bg="grey", fg="black")
        self.debug_entry.grid(row=0, column=1)
        self.debug_entry.insert(0, debug)

        self.acc_entry = tk.Entry(config_tab, bg="grey", fg="black")
        self.acc_entry.grid(row=1, column=1)
        self.acc_entry.insert(0, accuracy)

        self.wanted_path_entry = tk.Entry(config_tab, bg="grey", fg="black")
        self.wanted_path_entry.grid(row=2, column=1)
        self.wanted_path_entry.insert(0, wanted_path)

        self.device_w_entry = tk.Entry(config_tab, bg="grey", fg="black")
        self.device_w_entry.grid(row=3, column=1)
        self.device_w_entry.insert(0, device_w)

        self.device_h_entry = tk.Entry(config_tab, bg="grey", fg="black")
        self.device_h_entry.grid(row=4, column=1)
        self.device_h_entry.insert(0, device_h)

        self.screenshot_blank_entry = tk.Entry(config_tab, bg="grey", fg="black")
        self.screenshot_blank_entry.grid(row=5, column=1)
        self.screenshot_blank_entry.insert(0, screenshot_blank)

        self.adb_path_entry = tk.Entry(config_tab, bg="grey", fg="black")
        self.adb_path_entry.grid(row=6, column=1)
        self.adb_path_entry.insert(0, adb_path)

        self.event_mode_label = tk.Label(config_tab, text="活动模式").grid(row=7, column=0)
        self.event_mode_entry = tk.Entry(config_tab, bg="white", fg="black")
        self.event_mode_entry.insert(0, event_mode)
        self.event_mode_entry.grid(row=7, column=1)

        self.event_screenshot_label = tk.Label(config_tab, text="活动图标\n(开启活动模式)").grid(
            row=8, column=0
        )
        self.event_screenshot_entry = tk.Entry(config_tab, bg="white", fg="black")
        self.event_screenshot_entry.insert(0, event_screenshot)
        self.event_screenshot_entry.grid(row=8, column=1)

        self.raid_choose_label = tk.Label(config_tab, text="日常图标\n(关闭活动模式)").grid(
            row=9, column=0
        )
        self.raid_choose_entry = tk.Entry(config_tab, bg="white", fg="black")
        self.raid_choose_entry.insert(0, raid_choose)
        self.raid_choose_entry.grid(row=9, column=1)

        self.info_Label = tk.Label(config_tab, text="※不建议修改灰色部分").grid(row=10, column=1)
        self.save_button = tk.Button(
            config_tab, text="保存", command=self.save_config, width=10
        )
        self.save_button.grid(row=10, column=0)

        # 房主1
        self.fangzhu_device_label = tk.Label(fangzhu_tab, text="房主设备").grid(
            row=0, column=0
        )
        self.fangzhu_device_entry = tk.Entry(fangzhu_tab, bg="white", fg="black")
        self.fangzhu_device_entry.insert(0, fangzhu_device)
        self.fangzhu_device_entry.grid(row=0, column=1)

        self.limit_player_label = tk.Label(fangzhu_tab, text="最小玩家数").grid(
            row=1, column=0
        )
        self.limit_player_entry = tk.Entry(fangzhu_tab, bg="white", fg="black")
        self.limit_player_entry.insert(0, limit_player)
        self.limit_player_entry.grid(row=1, column=1)

        self.fangzhu_account_label = tk.Label(fangzhu_tab, text="房主截图").grid(
            row=2, column=0
        )
        self.fangzhu_account_entry = tk.Entry(fangzhu_tab, bg="white", fg="black")
        self.fangzhu_account_entry.insert(0, fangzhu_account)
        self.fangzhu_account_entry.grid(row=2, column=1)

        self.fangzhu_go_button = tk.Button(
            fangzhu_tab, text="GO!", command=lambda: self.fangzhu_go()
        ).grid(row=3, column=0)
        self.fangzhu_stop_button = tk.Button(
            fangzhu_tab, text="STOP!", command=lambda: self.fangzhu_stop()
        ).grid(row=3, column=1)
        self.fangzhu_scrollbar = ttk.Scrollbar(fangzhu_tab,orient=tk.VERTICAL)
        self.fangzhu_shell = tk.Text(fangzhu_tab, width=30, height=16, yscrollcommand=self.fangzhu_scrollbar.set)
        self.fangzhu_scrollbar.grid(row=4, column=3,sticky="nse")
        self.fangzhu_shell.grid(row = 4,columnspan=2)

        self.notebook.add(config_tab, text="全局设置")
        self.notebook.add(fangzhu_tab, text="房主")
        self.notebook.add(canzhan1_tab, text="参战1")
        self.notebook.add(canzhan2_tab, text="参战2")

        self.notebook.pack(fill=tk.BOTH, expand=1)

    def save_config(self):
        config["GENERAL"]["debug"] = self.debug_entry.get()
        config["GENERAL"]["accuracy"] = self.acc_entry.get()
        config["GENERAL"]["wanted_path"] = self.wanted_path_entry.get()
        config["GENERAL"]["device_w"] = self.device_w_entry.get()
        config["GENERAL"]["device_h"] = self.device_h_entry.get()
        config["GENERAL"]["screenshot_blank"] = self.screenshot_blank_entry.get()
        config["GENERAL"]["adb_path"] = self.adb_path_entry.get()
        config["RAID"]["event_mode"] = self.event_mode_entry.get()
        config["RAID"]["event_screenshot"] = self.event_screenshot_entry.get()
        config["RAID"]["raid_choose"] = self.raid_choose_entry.get()
        config["WF"]["fangzhu_device"] = self.fangzhu_device_entry.get()
        config["WF"]["limit_player"] = self.limit_player_entry.get()
        config["WF"]["fangzhu_account"] = self.fangzhu_account_entry.get()

        with open("./config.ini", "w") as configfile:
            config.write(configfile)

    def fangzhu_go(self):
        self.proc_fangzhu = subprocess.Popen(
            "python World_Flipper\\world_flipper_fangzhu.py",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.refreshText()

    def fangzhu_stop(self):
        self.proc_fangzhu.kill()
        print("[GUI]关闭房主子进程")

    def refreshText(self):
        # fangzhu_output = self.proc_fangzhu.stdout
        output, errors = self.proc_fangzhu.communicate()
        # self.fangzhu_shell.delete(0.0,tk.END)
        self.fangzhu_shell.insert(tk.INSERT, output)
        self.fangzhu_shell.update()
        self.after(500, self.refreshText)

    def on_closing(self):
        try:
            self.proc_fangzhu.kill()
            print("[GUI]退出时关闭所有子线程")
        except:
            print("[GUI]所有子线程已关闭")
        self.destroy()


if __name__ == "__main__":
    debug = config["GENERAL"].getint("debug")
    accuracy = config["GENERAL"].getfloat("accuracy")
    wanted_path = config["GENERAL"]["wanted_path"]
    screenshot_blank = config["GENERAL"].getfloat("screenshot_blank")
    adb_path = config["GENERAL"]["adb_path"]
    event_mode = config["RAID"]["event_mode"]
    event_screenshot = config["RAID"]["event_screenshot"]
    raid_choose = config["RAID"]["raid_choose"]
    fangzhu_device = config["WF"]["fangzhu_device"]
    limit_player = config["WF"].getint("limit_player")
    fangzhu_account = config["WF"]["fangzhu_account"]

    AutoPlayer_wf = AutoPlayer_WF()
    AutoPlayer_wf.mainloop()
