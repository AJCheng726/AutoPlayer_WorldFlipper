import os
import random
import threading
import time
from winsound import Beep

import cv2
import numpy
import pyautogui
from PIL import ImageGrab

from settings import *
from utils.Timer import Timer

# 桌面模式下的鼠标操作延迟，程序已经设置随机延迟这里无需设置修改
pyautogui.PAUSE = 0.1


# adb模式下设置连接测试
def adb_test():
    if mode == 1:
        return
    raw_content = os.popen("{0} devices".format(adb_path)).read()
    row_list = raw_content.split("List of devices attached\n")[1].split("\n")
    devices_list = [i for i in row_list if len(i) > 1]
    print(raw_content)
    return devices_list


# 截屏并发送到目录./screen, 默认返回cv2读取后的图片
def screen_shot(device=None):
    if device == None:
        a = "{0} shell screencap -p sdcard/screen.jpg".format(adb_path)
        b = "{0} pull sdcard/screen.jpg ./screen".format(adb_path)
    else:
        a = "{2} -s {0} shell screencap -p sdcard/screen_{1}.jpg".format(
            device, device, adb_path
        )
        b = "{2} -s {0} pull sdcard/screen_{1}.jpg ./screen".format(
            device, device, adb_path
        )
    for row in [a, b]:
        time.sleep(0.1)
        raw_content = os.popen(row).read()

    if device == None:
        screen = cv2.imread("./screen/screen.jpg")
    else:
        screen = cv2.imread("./screen/screen_{0}.jpg".format(device))
    return screen


# ADB命令模拟点击屏幕，参数pos为目标坐标(x, y)
def touch(pos, device=None):
    x, y = pos
    if device == None:
        a = "{2} shell input touchscreen tap {0} {1}".format(x, y, adb_path)
    else:
        a = "{3} -s {2} shell input touchscreen tap {0} {1}".format(
            x, y, device, adb_path
        )
    os.popen(a)


# 蜂鸣报警器，参数n为鸣叫次数，可用于提醒出错或任务完成
def alarm(n=3):
    frequency = 1500
    last = 500
    for n in range(n):
        Beep(frequency, last)
        time.sleep(0.05)


# 按cv2读取文件内容，匹配精度，图片名称】格式批量读取要查找的目标图片，名称为文件名
def load_imgs():
    imgs = {}
    treshold = accuracy
    path = wanted_path
    file_list = os.listdir(path)

    for file in file_list:
        name = file.split(".")[0]
        file_path = path + "/" + file
        a = [cv2.imread(file_path), treshold, name]
        imgs[name] = a

    return imgs


imgs = load_imgs()

# 在背景查找目标图片，以列表形式返回查找目标的中心坐标，
# screen是截屏图片，wanted是找的图片【按上面load_imgs的格式】，show是否以图片形式显示匹配结果【调试用】


def locate(screen, wanted, show=0):
    loc_pos = []
    wanted, treshold, c_name = wanted
    result = cv2.matchTemplate(screen, wanted, cv2.TM_CCOEFF_NORMED)
    location = numpy.where(result >= treshold)

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


# 裁剪图片以缩小匹配范围，screen为原图内容，upleft、downright是目标区域的左上角、右下角坐标


def cut(screen, upleft, downright):
    a, b = upleft
    c, d = downright
    screen = screen[b:d, a:c]
    return screen


# 随机偏移坐标，防止游戏的外挂检测。p是原坐标(x, y)，w、n是目标图像宽高，返回目标范围内的一个随机坐标


def random_offset(p, w=40, h=20):
    a, b = p
    w, h = int(w / 3), int(h / 3)
    c, d = random.randint(-w, w), random.randint(-h, h)
    e, f = a + c, b + d
    y = [e, f]
    return y


# 随机延迟点击，防止游戏外挂检测，延迟时间范围为【x, y】秒之间


def random_delay(x=0.1, y=0.2):
    t = random.uniform(x, y)
    time.sleep(t)


# 寻找目标 不点击
def find(target, device=None):
    screen = screen_shot(device)
    if debug:
        print("[find] 寻找目标并点击", target)
    wanted = imgs[target]
    size = wanted[0].shape
    h, w, ___ = size
    pts = locate(screen, wanted)
    if pts:
        if debug:
            print("[find] Y 已找到目标 ", target)
        xx = pts[0]
        return True
    else:
        if debug:
            print("[find] N 未找到目标 ", target)
        return False


# 寻找并点击, tap为FALSE则只寻找不点击，返回结果是否找到TURE/FALSE
def find_touch(target, device=None):
    screen = screen_shot(device)
    if debug:
        print("[find_touch] 寻找目标并点击", target)
    wanted = imgs[target]
    size = wanted[0].shape
    h, w, ___ = size
    pts = locate(screen, wanted)
    if pts:
        if debug:
            print("[find_touch] 已找到目标 ", target, pts)
        xx = pts[0]
        touch(xx, device=device)
        return True
    else:
        if debug:
            print("[find_touch] 未找到目标 ", target)
        return False


# 出现target返回true，超时返回false
def wait(target, device=None, max_wait_time=None):
    if debug:
        print("\r[wait] 等待目标", target, end="")
    timer = Timer()
    wanted = imgs[target]
    size = wanted[0].shape
    h, w, ___ = size

    while True:
        duration = timer.get_duration()
        if debug:
            print("\r > wait %s ... %ds " % (target, duration), end="")
        if max_wait_time is not None and 0 < max_wait_time < duration:
            if debug:
                print(" 超时", flush=True)
            return False

        screen = screen_shot(device=device)
        pts = locate(screen, wanted)
        if pts:
            if debug:
                print("\r[wait] 已找到目标 ", target, pts)
            xx = pts[0]
            touch(xx, device=device)
            return True
        time.sleep(screenshot_blank)


# 直至出现target再点击，超过max_wait_time则报错
def wait_touch(target, tap=True, device=None, max_wait_time=None):
    if debug:
        print("[wait_touch] 等待目标", target, end="")
    timer = Timer()
    wanted = imgs[target]
    size = wanted[0].shape
    h, w, ___ = size

    while True:
        duration = timer.get_duration()
        if debug:
            print("\r[wait_touch] wait %s ... %ds " % (target, duration), end="")
        if max_wait_time is not None and 0 < max_wait_time < duration:
            if debug:
                print(" 超时", flush=True)
            return False

        screen = screen_shot(device=device)
        pts = locate(screen, wanted)
        if pts:
            if debug:
                print("\r[wait_touch] 已找到目标 ", target)
            xx = pts[0]
            if tap:
                touch(xx, device=device)
            return True
        time.sleep(screenshot_blank)


# 寻找并点击,找到返回目标名，未找到返回NONE
def wait_list(target_list, max_wait_time=10):
    timer = Timer()
    screen = screen_shot()
    if debug:
        print("目标列表 ", target_list)
    re = None
    while True:
        duration = timer.get_duration()
        if debug:
            print("\r > wait %s ... %ds " % (target, duration), end="")
        if max_wait_time is not None and 0 < max_wait_time < duration:
            if debug:
                print(" 超时", flush=True)
            return

        for target in target_list:
            wanted = imgs[target]
            size = wanted[0].shape
            h, w, ___ = size
            pts = locate(screen, wanted)
            if pts:
                if debug:
                    print("[wait_list] 已找到目标 ", target, "位置 ", pts[0])
                xx = pts[0]
                re = target
                return target
