from distutils import command
import os
from re import search
import time
import configparser
import subprocess
import tkinter as tk
import ttkbootstrap as ttk
import ctypes
import webbrowser
from tkinter.ttk import Notebook
from ttkbootstrap.constants import *

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ApWF_GUI")


class AutoPlayer_WF(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap("./wanted/cover.ico")
        self.title("Auto Player WORLD FLIPPER")
        self.geometry("240x230")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.notebook = Notebook(self)

        config_tab = ttk.Frame(self.notebook)
        fangzhu_tab = ttk.Frame(self.notebook)
        canzhan_tab = ttk.Frame(self.notebook)
        danren_tab = ttk.Frame(self.notebook)
        gongju_tab = ttk.Frame(self.notebook)

        # 主页
        tk.Label(config_tab, text="Debug设置").grid(row=0, column=0)
        tk.Label(config_tab, text="图片匹配精度").grid(row=1, column=0)
        # self.wanted_path_label = tk.Label(config_tab, text="目标图片地址").grid(
        #     row=2, column=0
        # )
        # self.device_w_label = tk.Label(config_tab, text="设备宽").grid(row=3, column=0)
        # self.device_h_label = tk.Label(config_tab, text="设备高").grid(row=4, column=0)
        tk.Label(config_tab, text="截图间隔").grid(row=5, column=0)
        # self.adb_path_label = tk.Label(config_tab, text="ADB路径").grid(row=6, column=0)

        self.debug_entry = tk.Entry(config_tab)
        self.debug_entry.grid(row=0, column=1)
        self.debug_entry.insert(0, debug)

        self.acc_entry = tk.Entry(config_tab)
        self.acc_entry.grid(row=1, column=1)
        self.acc_entry.insert(0, accuracy)

        # self.wanted_path_entry = tk.Entry(config_tab)
        # self.wanted_path_entry.grid(row=2, column=1)
        # self.wanted_path_entry.insert(0, wanted_path)

        # self.device_w_entry = tk.Entry(config_tab)
        # self.device_w_entry.grid(row=3, column=1)
        # self.device_w_entry.insert(0, device_w)

        # self.device_h_entry = tk.Entry(config_tab)
        # self.device_h_entry.grid(row=4, column=1)
        # self.device_h_entry.insert(0, device_h)

        self.screenshot_blank_entry = tk.Entry(config_tab)
        self.screenshot_blank_entry.grid(row=5, column=1)
        self.screenshot_blank_entry.insert(0, screenshot_blank)

        # self.adb_path_entry = tk.Entry(config_tab)
        # self.adb_path_entry.grid(row=6, column=1)
        # self.adb_path_entry.insert(0, adb_path)

        tk.Label(config_tab, text="超时重启(秒)").grid(row=6, column=0)
        self.timeout_entry = tk.Entry(config_tab)
        self.timeout_entry.insert(0, timeout)
        self.timeout_entry.grid(row=6, column=1)

        tk.Label(config_tab, text="😏 ApWF version 1.9.1").grid(row=10, column=1)
        ttk.Button(config_tab, text="SAVE", command=self.save_config, width=5).grid(row=10, column=0, pady=2)

        tk.Label(config_tab, text="搜盘se子tu").grid(row=11, column=0)
        self.search_entry = tk.Entry(config_tab)
        self.search_entry.insert(0, "摩天楼")
        self.search_entry.grid(row=11, column=1)

        ttk.Button(
            config_tab, text="NGA", bootstyle=SUCCESS, command=lambda: self.open_NGA(self.search_entry.get()), width=4
        ).grid(row=12, columnspan=2, sticky=tk.W, padx=2, pady=5)
        ttk.Button(
            config_tab, text="B站", bootstyle=PRIMARY, command=lambda: self.open_BLBL(self.search_entry.get()), width=4
        ).grid(row=12, columnspan=2, sticky=tk.W, padx=60, pady=5)
        ttk.Button(
            config_tab, text="WIKI", bootstyle=DANGER, command=lambda: self.open_WIKI(self.search_entry.get()), width=4
        ).grid(row=12, column=1, sticky=tk.W, padx=38, pady=5)
        ttk.Button(config_tab, text="P站", bootstyle=DARK, command=lambda: self.open_PIXIV(self.search_entry.get()), width=4).grid(
            row=12, column=1, sticky=tk.E, pady=5
        )

        # 房主
        tk.Label(fangzhu_tab, text="房主设备").grid(row=0, column=0)
        self.fangzhu_device_entry = tk.Entry(fangzhu_tab)
        self.fangzhu_device_entry.insert(0, fangzhu_device)
        self.fangzhu_device_entry.grid(row=0, column=1)

        tk.Label(fangzhu_tab, text="最小玩家数").grid(row=1, column=0)
        self.limit_player_entry = tk.Entry(fangzhu_tab, width=5)
        self.limit_player_entry.insert(0, limit_player)
        self.limit_player_entry.grid(row=1, column=1, sticky=tk.W)

        tk.Label(fangzhu_tab, text="随机招募").grid(row=1, column=1, sticky=tk.E, padx=40)
        self.allow_stranger_entry = tk.Entry(fangzhu_tab, width=5)
        self.allow_stranger_entry.insert(0, allow_stranger)
        self.allow_stranger_entry.grid(row=1, column=1, sticky=tk.E)

        tk.Label(fangzhu_tab, text="活动模式").grid(row=4, column=0)
        self.event_mode_entry = tk.Entry(fangzhu_tab, width=5)
        self.event_mode_entry.insert(0, event_mode)
        self.event_mode_entry.grid(row=4, column=1, sticky=tk.W)

        tk.Label(fangzhu_tab, text="Raid难度").grid(row=4, column=1, sticky=tk.E, padx=40)
        self.raid_rank_entry = tk.Entry(fangzhu_tab, width=5)
        self.raid_rank_entry.insert(0, raid_rank)
        self.raid_rank_entry.grid(row=4, column=1, sticky=tk.E)

        tk.Label(fangzhu_tab, text="活动目标\n(开启活动模式)").grid(row=6, column=0)
        self.event_screenshot_entry = tk.Entry(fangzhu_tab)
        self.event_screenshot_entry.insert(0, event_screenshot)
        self.event_screenshot_entry.grid(row=6, column=1)

        tk.Label(fangzhu_tab, text="日常目标\n(关闭活动模式)").grid(row=7, column=0)
        self.raid_choose_entry = tk.Entry(fangzhu_tab)
        self.raid_choose_entry.insert(0, raid_choose)
        self.raid_choose_entry.grid(row=7, column=1)

        tk.Button(fangzhu_tab, text="GO!", width=7, command=lambda: self.fangzhu_go()).grid(row=99, column=1, sticky=tk.W, padx=5)
        tk.Button(fangzhu_tab, text="STOP!", width=7, command=lambda: self.fangzhu_stop()).grid(
            row=99, column=1, sticky=tk.E, padx=5
        )
        # self.fangzhu_scrollbar = ttk.Scrollbar(fangzhu_tab, orient=tk.VERTICAL)
        # self.fangzhu_shell = tk.Text(
        #     fangzhu_tab, width=30, height=18, yscrollcommand=self.fangzhu_scrollbar.set
        # )
        # self.fangzhu_scrollbar.grid(row=4, column=3, sticky="nse")
        # self.fangzhu_shell.grid(row=4, columnspan=2)

        # 参战
        tk.Label(canzhan_tab, text="房主截图").grid(row=0, column=0)
        self.fangzhu_account_entry = tk.Entry(canzhan_tab)
        self.fangzhu_account_entry.insert(0, fangzhu_account)
        self.fangzhu_account_entry.grid(row=0, column=1)

        tk.Label(canzhan_tab, text="战斗超时(秒)").grid(row=1, column=0)
        self.battle_timeout_entry = tk.Entry(canzhan_tab)
        self.battle_timeout_entry.insert(0, battle_timeout)
        self.battle_timeout_entry.grid(row=1, column=1)

        tk.Label(canzhan_tab, text="参战1设备").grid(row=10, column=0)
        self.canzhan1_device_entry = tk.Entry(canzhan_tab)
        self.canzhan1_device_entry.insert(0, canzhan1_device)
        self.canzhan1_device_entry.grid(row=10, column=1)

        tk.Button(canzhan_tab, text="GO!", width=7, command=lambda: self.canzhan1_go()).grid(
            row=11, column=1, sticky=tk.W, padx=5, pady=5
        )
        tk.Button(canzhan_tab, text="STOP!", width=7, command=lambda: self.canzhan1_stop()).grid(
            row=11, column=1, sticky=tk.E, padx=5, pady=5
        )

        tk.Label(canzhan_tab, text="参战2设备").grid(row=20, column=0)
        self.canzhan2_device_entry = tk.Entry(canzhan_tab)
        self.canzhan2_device_entry.insert(0, canzhan2_device)
        self.canzhan2_device_entry.grid(row=20, column=1)

        tk.Button(canzhan_tab, text="GO!", width=7, command=lambda: self.canzhan2_go()).grid(
            row=21, column=1, sticky=tk.W, padx=5, pady=5
        )
        tk.Button(canzhan_tab, text="STOP!", width=7, command=lambda: self.canzhan2_stop()).grid(
            row=21, column=1, sticky=tk.E, padx=5, pady=5
        )

        # 单人
        tk.Label(danren_tab, text="连战设备").grid(row=0, column=0)
        self.loop_device_entry = tk.Entry(danren_tab)
        self.loop_device_entry.insert(0, loop_device)
        self.loop_device_entry.grid(row=0, column=1)

        tk.Button(danren_tab, text="GO!", width=7, command=lambda: self.loop_go()).grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=3
        )
        tk.Button(danren_tab, text="STOP!", width=7, command=lambda: self.loop_stop()).grid(
            row=1, column=1, sticky=tk.E, padx=5, pady=3
        )

        tk.Label(danren_tab, text="连战设备2").grid(row=2, column=0)
        self.loop2_device_entry = tk.Entry(danren_tab)
        self.loop2_device_entry.insert(0, loop_device_2)
        self.loop2_device_entry.grid(row=2, column=1)

        tk.Button(danren_tab, text="GO!", width=7, command=lambda: self.loop2_go()).grid(
            row=3, column=1, sticky=tk.W, padx=5, pady=3
        )
        tk.Button(danren_tab, text="STOP!", width=7, command=lambda: self.loop2_stop()).grid(
            row=3, column=1, sticky=tk.E, padx=5, pady=3
        )

        tk.Label(danren_tab, text="蹭铃铛设备").grid(row=10, column=0)
        self.lingdang_device_entry = tk.Entry(danren_tab)
        self.lingdang_device_entry.insert(0, ring_device)
        self.lingdang_device_entry.grid(row=10, column=1)

        tk.Label(danren_tab, text="蹭铃铛目标").grid(row=11, column=0)
        self.ring_raid_choose_entry = tk.Entry(danren_tab)
        self.ring_raid_choose_entry.insert(0, ring_raid_choose)
        self.ring_raid_choose_entry.grid(row=11, column=1)

        tk.Button(danren_tab, text="GO!", width=7, command=lambda: self.ring_go()).grid(
            row=12, column=1, sticky=tk.W, padx=5, pady=3
        )
        tk.Button(danren_tab, text="STOP!", width=7, command=lambda: self.ring_stop()).grid(
            row=12, column=1, sticky=tk.E, padx=5, pady=3
        )

        # 工具箱
        tk.Label(gongju_tab, text="关机倒计时").grid(row=0, column=0)
        self.auto_shutdown_entry = tk.Entry(gongju_tab)
        self.auto_shutdown_entry.insert(0, "3600")
        self.auto_shutdown_entry.grid(row=0, column=1)

        tk.Button(gongju_tab, text="SET!", width=7, command=lambda: self.set_autoshutdown()).grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=5
        )
        tk.Button(
            gongju_tab,
            text="CANCEL!",
            width=7,
            command=lambda: self.cancel_autoshutdown(),
        ).grid(row=1, column=1, sticky=tk.E, padx=5, pady=5)

        tk.Button(gongju_tab, text="查询子进程状态", width=12, command=lambda: self.check_process()).grid(
            row=11, columnspan=2, sticky=tk.W, padx=5, pady=5
        )
        tk.Button(gongju_tab, text="关闭所有子进程", width=12, command=lambda: self.kill_process()).grid(
            row=11, columnspan=2, sticky=tk.E, padx=5, pady=5
        )
        tk.Button(gongju_tab, text="查询所有设备", width=12, command=lambda: self.check_devices()).grid(
            row=12, columnspan=2, sticky=tk.W, padx=5, pady=5
        )
        tk.Button(gongju_tab, text="所有设备截图", width=12, command=lambda: self.devices_screenshot()).grid(
            row=12, columnspan=2, sticky=tk.E, padx=5, pady=5
        )

        # notebook
        self.notebook.add(config_tab, text="主页")
        self.notebook.add(fangzhu_tab, text="房主")
        self.notebook.add(canzhan_tab, text="参战")
        self.notebook.add(danren_tab, text="单人")
        self.notebook.add(gongju_tab, text="工具箱")

        self.notebook.pack(fill=tk.BOTH, expand=1)

    def save_config(self):
        config["GENERAL"]["debug"] = self.debug_entry.get()
        config["GENERAL"]["accuracy"] = self.acc_entry.get()
        # config["GENERAL"]["wanted_path"] = self.wanted_path_entry.get()
        # config["GENERAL"]["device_w"] = self.device_w_entry.get()
        # config["GENERAL"]["device_h"] = self.device_h_entry.get()
        config["GENERAL"]["screenshot_blank"] = self.screenshot_blank_entry.get()
        # config["GENERAL"]["adb_path"] = self.adb_path_entry.get()
        config["RAID"]["event_mode"] = self.event_mode_entry.get()
        config["RAID"]["event_screenshot"] = self.event_screenshot_entry.get()
        config["RAID"]["raid_choose"] = self.raid_choose_entry.get()
        config["RAID"]["ring_raid_choose"] = self.ring_raid_choose_entry.get()
        config["RAID"]["raid_rank"] = self.raid_rank_entry.get()
        config["WF"]["fangzhu_device"] = self.fangzhu_device_entry.get()
        config["WF"]["limit_player"] = self.limit_player_entry.get()
        config["WF"]["fangzhu_account"] = self.fangzhu_account_entry.get()
        config["WF"]["canzhan_device_1"] = self.canzhan1_device_entry.get()
        config["WF"]["canzhan_device_2"] = self.canzhan2_device_entry.get()
        config["WF"]["timeout"] = self.timeout_entry.get()
        config["WF"]["battle_timeout"] = self.battle_timeout_entry.get()
        config["WF"]["loop_device"] = self.loop_device_entry.get()
        config["WF"]["loop_device_2"] = self.loop2_device_entry.get()
        config["WF"]["allow_stranger"] = self.allow_stranger_entry.get()
        config["WF"]["ring_device"] = self.lingdang_device_entry.get()

        with open("./config.ini", "w") as configfile:
            config.write(configfile)

    def fangzhu_go(self):
        self.save_config()
        self.proc_fangzhu = subprocess.Popen("python World_Flipper\\world_flipper_fangzhu.py")

    def canzhan1_go(self):
        self.save_config()
        self.proc_canzhan1 = subprocess.Popen("python World_Flipper\\world_flipper_canzhan1.py")

    def canzhan2_go(self):
        self.save_config()
        self.proc_canzhan2 = subprocess.Popen(
            "python World_Flipper\\world_flipper_canzhan2.py",
            # shell=False,
            # stdout=subprocess.PIPE,
            # stderr=subprocess.STDOUT,
            # encoding="GBK",
        )

    def loop_go(self):
        self.save_config()
        self.proc_loop = subprocess.Popen("python World_Flipper\\world_flipper_loop.py")

    def loop2_go(self):
        self.save_config()
        self.proc_loop2 = subprocess.Popen("python World_Flipper\\world_flipper_loop_2.py")

    def ring_go(self):
        self.save_config()
        self.proc_ring = subprocess.Popen("python World_Flipper\\world_flipper_ring.py")

    def fangzhu_stop(self):
        try:
            self.proc_fangzhu.kill()
            print("[GUI]房主子进程已关闭")
        except:
            print("[GUI]房主子进程未启动")

    def canzhan1_stop(self):
        try:
            self.proc_canzhan1.kill()
            print("[GUI]参战1子进程已关闭")
        except:
            print("[GUI]参战1子进程未启动")

    def canzhan2_stop(self):
        try:
            self.proc_canzhan2.kill()
            print("[GUI]参战2子进程已关闭")
        except:
            print("[GUI]参战2子进程未启动")

    def loop_stop(self):
        try:
            self.proc_loop.kill()
            print("[GUI]单人连战子进程已关闭")
        except:
            print("[GUI]单人连战子进程未启动")

    def loop2_stop(self):
        try:
            self.proc_loop2.kill()
            print("[GUI]单人连战2子进程已关闭")
        except:
            print("[GUI]单人连战2子进程未启动")

    def ring_stop(self):
        try:
            self.proc_ring.kill()
            print("[GUI]蹭铃铛子进程已关闭")
        except:
            print("[GUI]蹭铃铛子进程未启动")

    def refreshText(self, p, text):
        fangzhu_output = self.proc_fangzhu.stdout

        for line in iter(fangzhu_output.readline(1), b""):
            print(line)
            # self.fangzhu_shell.insert(tk.INSERT, line)
        # self.fangzhu_shell.delete(0.0,tk.END)
        self.fangzhu_shell.update()
        self.fangzhu_shell.see(tk.END)
        self.after(500, self.refreshText)

    def check_process(self):
        print("[GUI]查询所有子进程")
        try:
            print("[GUI]房主子进程", self.proc_fangzhu.poll())
        except:
            print("[GUI]房主子进程未启动")
        try:
            print("[GUI]参战1子进程", self.proc_canzhan1.poll())
        except:
            print("[GUI]参战1子进程未启动")
        try:
            print("[GUI]参战2子进程", self.proc_canzhan2.poll())
        except:
            print("[GUI]参战2子进程未启动")
        try:
            print("[GUI]单人连战子进程", self.proc_loop.poll())
        except:
            print("[GUI]单人连战子进程未启动")
        try:
            print("[GUI]单人连战2子进程", self.proc_loop2.poll())
        except:
            print("[GUI]单人连战2子进程未启动")
        try:
            print("[GUI]蹭铃铛子进程", self.proc_ring.poll())
        except:
            print("[GUI]蹭铃铛子进程未启动")

    def kill_process(self):
        print("[GUI]关闭所有子进程")
        self.fangzhu_stop()
        self.canzhan1_stop()
        self.canzhan2_stop()
        self.loop_stop()
        self.loop2_stop()
        self.ring_stop()

    def check_devices(self):
        subprocess.Popen("{0} devices".format(adb_path))

    def devices_screenshot(self):
        for d in list(set([fangzhu_device, canzhan1_device, canzhan2_device, loop_device, ring_device])):
            a = "{2} -s {0} shell screencap -p sdcard/screen_{1}.jpg".format(d, d, adb_path)
            b = "{2} -s {0} pull sdcard/screen_{1}.jpg ./screen".format(d, d, adb_path)
            for row in [a, b]:
                raw_content = os.popen(row).read()
                # time.sleep(0.2)
            print("[GUI]已对设备{0}截图".format(d))

    def set_autoshutdown(self):
        subprocess.Popen("shutdown -s -t " + self.auto_shutdown_entry.get())

    def cancel_autoshutdown(self):
        subprocess.Popen("shutdown -a")

    def on_closing(self):
        self.kill_process()
        self.destroy()

    def open_NGA(self, search):
        webbrowser.open("https://bbs.nga.cn/thread.php?key={0}&fid=693".format(search), new=0)

    def open_BLBL(self, search):
        webbrowser.open("https://bilibili.com/search?keyword=世界弹射物语 {0}".format(search), new=0)

    def open_WIKI(self, search):
        webbrowser.open("http://sjtswy.gamer.cc/search?word={0}&type=0".format(search), new=0)
    def open_PIXIV(self, search):
        webbrowser.open("https://www.pixiv.net/tags/{0}/artworks?s_mode=s_tag".format(search), new=0)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("./config.ini")

    debug = config["GENERAL"].getint("debug")
    accuracy = config["GENERAL"].getfloat("accuracy")
    wanted_path = config["GENERAL"]["wanted_path"]
    screenshot_blank = config["GENERAL"].getfloat("screenshot_blank")
    adb_path = config["GENERAL"]["adb_path"]
    device_w = config["GENERAL"].getint("device_w")
    device_h = config["GENERAL"].getint("device_h")

    fangzhu_device = config["WF"]["fangzhu_device"]
    limit_player = config["WF"].getint("limit_player")
    fangzhu_account = config["WF"]["fangzhu_account"]
    canzhan1_device = config["WF"]["canzhan_device_1"]
    canzhan2_device = config["WF"]["canzhan_device_2"]
    loop_device = config["WF"]["loop_device"]
    loop_device_2 = config["WF"]["loop_device_2"]
    ring_device = config["WF"]["ring_device"]
    timeout = config["WF"].getint("timeout")
    battle_timeout = config["WF"].getint("battle_timeout")
    allow_stranger = config["WF"].getint("allow_stranger")

    event_mode = config["RAID"]["event_mode"]
    raid_rank = config["RAID"]["raid_rank"]
    event_screenshot = config["RAID"]["event_screenshot"]
    raid_choose = config["RAID"]["raid_choose"]
    ring_raid_choose = config["RAID"]["ring_raid_choose"]

    AutoPlayer_wf = AutoPlayer_WF()
    AutoPlayer_wf.mainloop()
