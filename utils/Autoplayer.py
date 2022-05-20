import os
import re
import subprocess
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
        disable_init=False,
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
        self.disable_init = disable_init

        if not disable_init:
            self.imgs = self.load_imgs()
            self.adb_connect()

    def devices_check(self):
        # adb模式下设置连接测试
        raw_content = os.popen("{0} devices".format(self.adb_path)).read()
        # print(raw_content)
        deivces_list = raw_content.split("List of devices attached\n")[1].split("\n")
        deivces_list = [i for i in deivces_list if len(i) > 1]
        devices_dict = {}
        for device_and_sit in deivces_list:
            devices_dict[device_and_sit.split("\t")[0]] = device_and_sit.split("\t")[1]
        return devices_dict

    def adb_connect(self):
        # 连接adb
        try:
            devices_dict = self.devices_check()
            if devices_dict[self.use_device] == "devcice":
                print("{0}已连接adb".format(self.use_device))
                return
        except:
            print("与{0}建立adb连接...".format(self.use_device))
            self.adb_disconnect()
            feedback = os.popen("{0} connect {1}".format(self.adb_path, self.use_device)).read()[:-1:]
            if "connected" not in feedback:
                print(feedback)
                print("尝试连接{0}失败...".format(self.use_device))

    def adb_disconnect(self):
        # 断开adb
        try:
            feedback = os.popen("{0} disconnect {1}".format(self.adb_path, self.use_device)).read()[:-1:]
            print(feedback)
        except:
            print("未发现设备{0}或无法断开".format(self.use_device))

    def start_app(self):
        if self.debug:
            print("[start_app] start apk", self.apk_name)
        cmd = "{3} -s {0} shell am start {1}/{2}".format(self.use_device, self.apk_name, self.active_class_name, self.adb_path)
        os.popen(cmd)

    def stop_app(self):
        if self.debug:
            print("[stop_app] stop app", self.apk_name)
        cmd = "{2} -s {0} shell am force-stop {1}".format(self.use_device, self.apk_name, self.adb_path)
        os.popen(cmd)

    def check_app(self):
        if self.debug:
            print("[check_app] check app", self.apk_name)
        cmd = "{2} -s {0} shell pidof {1}".format(self.use_device, self.apk_name, self.adb_path)
        raw_content = os.popen(cmd).read()
        if self.debug:
            print("[check_app] check app pid:", raw_content)
        if raw_content == "":
            return False
        else:
            return True

    def check_current_app(self):
        cmd = "{0} -s {1} shell dumpsys window | findstr mCurrentFocus".format(self.adb_path, self.use_device)
        current_apks = os.popen(cmd).read()
        current_apks = re.findall(r"u0 (.*)/",current_apks)
        if self.debug:
            print("[check_current_app] {0} currentfocus apk is {1}".format(self.use_device, current_apks))
        if self.apk_name in current_apks:
            return True
        else:
            return False

    def check_restart(self, restart_time):
        for time in restart_time:
            if datetime.now() > time:
                print("触发游戏重启时间...游戏重启...")
                self.stop_app()
                return True
        return False

    def screen_shot(self):
        # 截屏并发送到目录./screen, 默认返回cv2读取后的图片
        if ":" not in self.use_device:
            screenshot_name = self.use_device
        else:
            screenshot_name = self.use_device.split(":")[1]
        if self.use_device == None:
            raise Exception("[Error] 没有找到设备")
        else:
            a = "{2} -s {0} shell screencap -p sdcard/{1}.jpg".format(self.use_device, screenshot_name, self.adb_path)
            b = "{2} -s {0} pull sdcard/{1}.jpg ./screen".format(self.use_device, screenshot_name, self.adb_path)
        for row in [a, b]:
            time.sleep(0.1)
            raw_content = os.popen(row).read()

        screen = cv2.imread("./screen/{0}.jpg".format(screenshot_name))
        return screen

    def touch(self, pos):
        # ADB命令模拟点击屏幕，参数pos为目标坐标(x, y)
        if self.debug:
            print("[touch] touch {0}".format(pos))
        x, y = pos
        a = "{3} -s {2} shell input touchscreen tap {0} {1}".format(x, y, self.use_device, self.adb_path)
        os.popen(a)

    def swipe(self, pos1, pos2):
        if self.debug:
            print("[swipe] swipe from {0} to {1}".format(pos1, pos2))
        a = "{0} -s {1} shell input swipe {2} {3} {4} {5}".format(
            self.adb_path,
            self.use_device,
            pos1[0],
            pos1[1],
            pos2[0],
            pos2[1],
        )
        os.popen(a)

    def down_swipe(self, x_start=None, y_start=None, x_end=None, y_end=None):
        if x_start == None:
            x_start = (1 / 2) * self.device_w
        if y_start == None:
            y_start = (700 / 960) * self.device_h
        if x_end == None:
            x_end = (1 / 2) * self.device_w
        if y_end == None:
            y_end = (500 / 960) * self.device_h

        a = "{0} -s {1} shell input swipe {2} {3} {4} {5}".format(
            self.adb_path,
            self.use_device,
            (1 / 2) * self.device_w,
            (700 / 960) * self.device_h,
            (1 / 2) * self.device_w,
            (500 / 960) * self.device_h,
        )
        os.popen(a)

    def alarm(self, n=3):
        # 蜂鸣报警器，参数n为鸣叫次数，可用于提醒出错或任务完成
        frequency = 1500
        last = 500
        for n in range(n):
            Beep(frequency, last)
            time.sleep(0.05)

    def load_imgs(self):
        # 按cv2读取文件内容，匹配精度，图片名称格式批量读取要查找的目标图片，名称为文件名
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
            print("[load_imgs] 从{0}加载图片{1}".format(path, len(file_list)))

        return imgs

    def locate(self, screen, wanted, show=0):
        # 在背景查找目标图片，以列表形式返回查找目标的中心坐标
        loc_pos = []
        wanted, treshold, c_name = wanted
        try:
            result = cv2.matchTemplate(screen, wanted, cv2.TM_CCOEFF_NORMED)
            location = numpy.where(result >= treshold)
        except:
            raise Exception("获取screen失败，确认设备{0}没有多个子进程占用，wanted存在{1}".format(self.use_device, c_name))

        h, w = wanted.shape[:-1]

        n, ex, ey = 1, 0, 0
        for pt in zip(*location[::-1]):
            x, y = pt[0] + int(w / 2), pt[1] + int(h / 2)
            # if (x - ex) + (y - ey) < 15:  # 去掉邻近重复的点
            #     continue
            if (x - ex) < 0.05 * self.device_w and (y - ey) < 0.05 * self.device_h:  # 去掉邻近重复的点
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

    def find(self, target, threshold=None):
        # 寻找目标 不点击
        screen = self.screen_shot()
        if self.debug:
            print("[find] 寻找目标并点击", target)
        wanted = self.imgs[target]
        if threshold != None:  # 自定义阈值
            wanted[1] = threshold
        pts = self.locate(screen, wanted)
        if pts:
            if self.debug:
                print("[find] 已找到目标 ", target, pts)
            xx = pts[0]
            return True
        else:
            if self.debug:
                print("[find] 未找到目标 ", target)
            return False

    def find_location(self, target, threshold=None):
        # 寻找目标 不点击
        screen = self.screen_shot()
        if self.debug:
            print("[find] 寻找目标位置", target)
        wanted = self.imgs[target]
        if threshold != None:  # 自定义阈值
            wanted[1] = threshold
        pts = self.locate(screen, wanted)
        if pts:
            if self.debug:
                print("[find] 已找到目标 ", target, pts)
            xx = pts[0]
            return pts
        else:
            if self.debug:
                print("[find] 未找到目标 ", target)
            return None

    def find_any(self, target=[]):
        # 寻找多个目标，返回index，都没找到返回-1
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

    def find_touch(self, target, delay=0.5, threshold=None):
        # 寻找并点击, tap为FALSE则只寻找不点击，返回结果是否找到TURE/FALSE
        screen = self.screen_shot()
        if self.debug:
            print("[find_touch] 寻找目标并点击", target)
        wanted = self.imgs[target]
        if threshold != None:  # 自定义阈值
            wanted[1] = threshold
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

    def wait(self, target, max_wait_time=None, threshold=None):
        # 出现target返回true，超时返回false
        if self.debug:
            print("[wait] 等待目标", target)
        timer = Timer()
        wanted = self.imgs[target]
        if threshold != None:  # 自定义阈值
            wanted[1] = threshold
        size = wanted[0].shape
        h, w, ___ = size

        while True:
            duration = timer.get_duration()
            if self.debug:
                print("\r[wait] wait %s ... %ds " % (target, duration), end="")
            if max_wait_time is not None and 0 < max_wait_time < duration:
                if self.debug:
                    print("\n[wait] 超时")
                return False

            screen = self.screen_shot()
            pts = self.locate(screen, wanted)
            if pts:
                if self.debug:
                    print("\n[wait] 已找到目标 ", target, pts)
                xx = pts[0]
                # self.touch(xx)
                return True
            time.sleep(self.screenshot_blank)

    def wait_touch(self, target, max_wait_time=None, delay=0.5, threshold=None):
        # 直至出现target再点击，超过max_wait_time则报错
        if self.debug:
            print("[wait_touch] 等待目标", target)
        timer = Timer()
        wanted = self.imgs[target]
        if threshold != None:  # 自定义阈值
            wanted[1] = threshold
        size = wanted[0].shape
        h, w, ___ = size

        while True:
            duration = timer.get_duration()
            if self.debug:
                print("\r[wait_touch] wait ... %ds " % (duration), end="")
            if max_wait_time is not None and 0 < max_wait_time < duration:
                if self.debug:
                    print("\n[wait_touch] 超时")
                return False

            screen = self.screen_shot()
            pts = self.locate(screen, wanted)
            if pts:
                if self.debug:
                    print("\n[wait_touch] 已找到目标 ", target)
                xx = pts[0]
                time.sleep(delay)
                self.touch(xx)
                return True
            time.sleep(self.screenshot_blank)

    def wait_touch_list(self, target_list, max_wait_time=10, delay=0.5, threshold=None):
        timer = Timer()
        if self.debug:
            print("[wait_touch_list] 目标列表 ", target_list)
        re = None
        while True:
            duration = timer.get_duration()
            if self.debug:
                print("\r[wait_touch_list] wait ... %ds " % (duration), end="")
            if max_wait_time is not None and 0 < max_wait_time < duration:
                if self.debug:
                    print("\n[wait_touch_list] 超时")
                return

            screen = self.screen_shot()
            for target in target_list:
                wanted = self.imgs[target]
                if threshold != None:  # 自定义阈值
                    wanted[1] = threshold
                size = wanted[0].shape
                h, w, ___ = size
                pts = self.locate(screen, wanted)
                if pts:
                    if self.debug:
                        print("\n[wait_touch_list] 已找到目标 ", target, "位置 ", pts[0])
                    xx = pts[0]
                    re = target
                    time.sleep(delay)
                    self.touch(xx)
            time.sleep(self.screenshot_blank)

    def wait_list(self, target_list, max_wait_time=10, threshold=None):
        # 寻找并点击,找到返回目标名，未找到返回NONE
        timer = Timer()
        if self.debug:
            print("[wait_list] 目标列表 ", target_list)
        re = None
        while True:
            duration = timer.get_duration()
            if self.debug:
                print("\r[wait_list] wait ... %ds " % (duration), end="")
            if max_wait_time is not None and 0 < max_wait_time < duration:
                if self.debug:
                    print("\n[wait_list] 超时")
                return

            screen = self.screen_shot()
            for target in target_list:
                wanted = self.imgs[target]
                if threshold != None:  # 自定义阈值
                    wanted[1] = threshold
                size = wanted[0].shape
                h, w, ___ = size
                pts = self.locate(screen, wanted)
                if pts:
                    if self.debug:
                        print("\n[wait_list] 已找到目标 ", target, "位置 ", pts[0])
                    xx = pts[0]
                    re = target
                    return target

    def touch_with_checkpoint(self, target, checkpoint_start=None, sleeptime=0.5, checkpoint_end=None):
        if checkpoint_start != None:
            self.wait(checkpoint_start)
        time.sleep(sleeptime)
        while not self.find(checkpoint_end):
            self.find_touch(target)
            time.sleep(sleeptime)
        time.sleep(sleeptime)
        return True


if __name__ == "__main__":
    import configparser

    config = configparser.ConfigParser()
    config.read("./config.ini")

    player1 = Autoplayer(
        use_device="127.0.0.1:62001",
        adb_path=config["GENERAL"]["adb_path"],
        apk_name=config["WF"]["wf_apk_name"],
        active_class_name=config["WF"]["wf_active_class_name"],
        debug=1,
        disable_init=True,
    )
    print(player1.apk_name,player1.check_current_app())
