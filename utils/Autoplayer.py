import os
import random
import sys
import time
from datetime import datetime, timedelta
from winsound import Beep

import cv2
import numpy

sys.path.append("./")

from utils.Timer import Timer


class Autoplayer:
    def __init__(
        self,
        use_device,
        adb_path,
        apk_name,
        active_class_name,
        debug=0,
        accuracy=0.75,
        screenshot_blank=0.5,
        wanted_path="./wanted",
        device_w=540,
        device_h=960,
    ) -> None:
        self.use_device = use_device
        self.adb_path = adb_path
        self.apk_name = apk_name
        self.active_class_name = active_class_name
        self.debug = debug
        self.accuracy = accuracy
        self.screenshot_blank = screenshot_blank
        self.wanted_path = wanted_path
        self.device_w = device_w
        self.device_h = device_h

        self.imgs = self.load_imgs()
        self.adb_test()

    # adb模式下设置连接测试
    def adb_test(self):
        raw_content = os.popen("{0} devices".format(self.adb_path)).read()
        row_list = raw_content.split("List of devices attached\n")[1].split("\n")
        devices_list = [i for i in row_list if len(i) > 1]
        print(raw_content)
        return devices_list

    def start_app(self):
        if self.debug:
            print("[start_app] start apk", self.apk_name)
        cmd = "adb -s {0} shell am start {1}/{2}".format(
            self.use_device, self.apk_name, self.active_class_name
        )
        os.popen(cmd)

    def stop_app(self):
        if self.debug:
            print("[stop_app] stop app", self.apk_name)
        cmd = "adb -s {0} shell am force-stop {1}".format(
            self.use_device, self.apk_name
        )
        os.popen(cmd)

    def check_app(self):
        if self.debug:
            print("[check_app] check app", self.apk_name)
        cmd = "adb -s {0} shell pidof {1}".format(self.use_device, self.apk_name)
        raw_content = os.popen(cmd).read()
        if self.debug:
            print("[check_app] check app pid:", raw_content)
        if raw_content == "":
            return False
        else:
            return True

    def check_restart(self, restart_time):
        for time in restart_time:
            if datetime.now() > time:
                print("触发游戏重启时间...游戏重启...")
                self.stop_app()
                return True
        return False

    # 截屏并发送到目录./screen, 默认返回cv2读取后的图片
    def screen_shot(self):
        if self.use_device == None:
            raise Exception("[Error] 没有找到设备")
        else:
            a = "{2} -s {0} shell screencap -p sdcard/screen_{1}.jpg".format(
                self.use_device, self.use_device, self.adb_path
            )
            b = "{2} -s {0} pull sdcard/screen_{1}.jpg ./screen".format(
                self.use_device, self.use_device, self.adb_path
            )
        for row in [a, b]:
            time.sleep(0.1)
            raw_content = os.popen(row).read()

        screen = cv2.imread("./screen/screen_{0}.jpg".format(self.use_device))
        return screen

    # ADB命令模拟点击屏幕，参数pos为目标坐标(x, y)
    def touch(self, pos):
        x, y = pos
        a = "{3} -s {2} shell input touchscreen tap {0} {1}".format(
            x, y, self.use_device, self.adb_path
        )
        os.popen(a)

    def down_swipe(self):
        a = "{0} -s {1} shell input swipe {2} {3} {4} {5}".format(
            self.adb_path,
            self.use_device,
            (1 / 2) * self.device_w,
            (700 / 960) * self.device_h,
            (1 / 2) * self.device_w,
            (500 / 960) * self.device_h,
        )
        os.popen(a)

    # 蜂鸣报警器，参数n为鸣叫次数，可用于提醒出错或任务完成
    def alarm(self, n=3):
        frequency = 1500
        last = 500
        for n in range(n):
            Beep(frequency, last)
            time.sleep(0.05)

    # 按cv2读取文件内容，匹配精度，图片名称格式批量读取要查找的目标图片，名称为文件名
    def load_imgs(self):
        imgs = {}
        treshold = self.accuracy
        path = self.wanted_path
        file_list = os.listdir(path)

        for file in file_list:
            name = file.split(".")[0]
            file_path = path + "/" + file
            a = [cv2.imread(file_path), treshold, name]
            imgs[name] = a
        if self.debug:
            print("从{0}加载图片{1}".format(path, len(file_list)))

        return imgs

    # 在背景查找目标图片，以列表形式返回查找目标的中心坐标
    def locate(self, screen, wanted, show=0):
        loc_pos = []
        wanted, treshold, c_name = wanted
        try:
            result = cv2.matchTemplate(screen, wanted, cv2.TM_CCOEFF_NORMED)
            location = numpy.where(result >= treshold)
        except:
            raise Exception(
                "定位图像出错，确认以下信息...使用设备：", self.use_device, "且目标文件夹下存在图像：", c_name,
            )

        h, w = wanted.shape[:-1]

        n, ex, ey = 1, 0, 0
        for pt in zip(*location[::-1]):
            x, y = pt[0] + int(w / 2), pt[1] + int(h / 2)
            if (x - ex) + (y - ey) < 15:  # 去掉邻近重复的点
                continue
            ex, ey = x, y

            cv2.circle(screen, (x, y), 10, (0, 0, 255), 3)

            x, y = int(x), int(y)
            loc_pos.append([x, y])

        if show:  # 在图上显示寻找的结果，调试时开启
            cv2.imshow("we get", screen)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return loc_pos

    def cut(self, screen, upleft, downright):
        a, b = upleft
        c, d = downright
        screen = screen[b:d, a:c]
        return screen

    def random_offset(self, p, w=40, h=20):
        a, b = p
        w, h = int(w / 3), int(h / 3)
        c, d = random.randint(-w, w), random.randint(-h, h)
        e, f = a + c, b + d
        y = [e, f]
        return y

    def random_delay(self, x=0.1, y=0.2):
        t = random.uniform(x, y)
        time.sleep(t)

    # 寻找目标 不点击
    def find(self, target):
        screen = self.screen_shot()
        if self.debug:
            print("[find] 寻找目标并点击", target)
        wanted = self.imgs[target]
        pts = self.locate(screen, wanted)
        if pts:
            if self.debug:
                print("[find] 已找到目标 ", target)
            xx = pts[0]
            return True
        else:
            if self.debug:
                print("[find] 未找到目标 ", target)
            return False

    # 寻找多个目标，返回index，都没找到返回-1
    def find_any(self, target=[]):
        screen = self.screen_shot()
        if self.debug:
            print("[find_any] 寻找多个目标", target)
        for tgt in target:
            wanted = self.imgs[tgt]
            pts = self.locate(screen, wanted)
            if pts:
                if self.debug:
                    print("[find_any] 已找到目标 ", tgt)
                return target.index(tgt)
        if self.debug:
            print("[find_any] 未找到目标 ", target)
        return -1

    # 寻找并点击, tap为FALSE则只寻找不点击，返回结果是否找到TURE/FALSE
    def find_touch(self, target, delay=0.5):
        screen = self.screen_shot()
        if self.debug:
            print("[find_touch] 寻找目标并点击", target)
        wanted = self.imgs[target]
        size = wanted[0].shape
        h, w, ___ = size
        pts = self.locate(screen, wanted)
        if pts:
            if self.debug:
                print("[find_touch] 已找到目标 ", target, pts)
            xx = pts[0]
            time.sleep(delay)
            self.touch(xx)
            return True
        else:
            if self.debug:
                print("[find_touch] 未找到目标 ", target)
            return False

    # 出现target返回true，超时返回false
    def wait(self, target, max_wait_time=None):
        if self.debug:
            print("\r[wait] 等待目标", target, end="")
        timer = Timer()
        wanted = self.imgs[target]
        size = wanted[0].shape
        h, w, ___ = size

        while True:
            duration = timer.get_duration()
            if self.debug:
                print("\r > wait %s ... %ds " % (target, duration), end="")
            if max_wait_time is not None and 0 < max_wait_time < duration:
                if self.debug:
                    print(" 超时", flush=True)
                return False

            screen = self.screen_shot()
            pts = self.locate(screen, wanted)
            if pts:
                if self.debug:
                    print("\r[wait] 已找到目标 ", target, pts)
                xx = pts[0]
                # self.touch(xx)
                return True
            time.sleep(self.screenshot_blank)

    # 直至出现target再点击，超过max_wait_time则报错
    def wait_touch(self, target, max_wait_time=None, delay=0.5):
        if self.debug:
            print("[wait_touch] 等待目标", target, end="")
        timer = Timer()
        wanted = self.imgs[target]
        size = wanted[0].shape
        h, w, ___ = size

        while True:
            duration = timer.get_duration()
            if self.debug:
                print("\r[wait_touch] wait %s ... %ds " % (target, duration), end="")
            if max_wait_time is not None and 0 < max_wait_time < duration:
                if self.debug:
                    print(" 超时", flush=True)
                return False

            screen = self.screen_shot()
            pts = self.locate(screen, wanted)
            if pts:
                if self.debug:
                    print("\r[wait_touch] 已找到目标 ", target)
                xx = pts[0]
                time.sleep(delay)
                self.touch(xx)
                return True
            time.sleep(self.screenshot_blank)

    # 寻找并点击,找到返回目标名，未找到返回NONE
    def wait_list(self, target_list, max_wait_time=10):
        timer = Timer()
        screen = self.screen_shot()
        if self.debug:
            print("目标列表 ", target_list)
        re = None
        while True:
            duration = timer.get_duration()
            if self.debug:
                print("\r > wait %s ... %ds " % (target, duration), end="")
            if max_wait_time is not None and 0 < max_wait_time < duration:
                if self.debug:
                    print(" 超时", flush=True)
                return

            for target in target_list:
                wanted = self.imgs[target]
                size = wanted[0].shape
                h, w, ___ = size
                pts = self.locate(screen, wanted)
                if pts:
                    if self.debug:
                        print("[wait_list] 已找到目标 ", target, "位置 ", pts[0])
                    xx = pts[0]
                    re = target
                    return target


if __name__ == "__main__":
    # from settings import *
    import configparser

    config = configparser.ConfigParser()
    # config.sections()
    config.read("./config.ini")
    # print(config['GENERAL']['Debug'])
    # config["RAID"]["event_screenshot"] = "raid_event2"
    # config["WF"]["fangzhu_account"] = "icon_chufaqianpickup,icon_chufaqian"
    # print("修改后的参数", config["RAID"]["event_screenshot"])
    # with open("example.ini", "w") as configfile:
    #     config.write(configfile)

    player1 = Autoplayer(
        use_device="emulator-5554",
        adb_path=config["GENERAL"]["adb_path"],
        apk_name=config["WF"]["wf_apk_name"],
        active_class_name=config["WF"]["wf_active_class_name"],
    )
    player2 = Autoplayer(
        use_device="emulator-5556",
        adb_path="toolkits\\ADB\\adb.exe",
        apk_name="com.leiting.wf",
        active_class_name="air.com.leiting.wf.AppEntry",
    )

    # player1.stop_app()
    # player1.start_app()
    # print(player1.check_app())
    player1.screen_shot()
    player2.screen_shot()
    # player1.wait_touch("raid_event1")
