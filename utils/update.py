import sys
from tkinter import E
import git

sys.path.append("./utils/")
sys.path.append("./")
import print_color
import Timer
from utils.print_color import printGreen, printPink, printRed

timer = Timer.Timer()
try:
    printPink("{0} ApWF正在从git更新...第一次更新根据网络情况需要10-20分钟".format(timer.simple_time()))
    repo = git.Repo("./")
    remote = repo.remote()
    info = remote.pull()
    for i in info:
        print(i)
    printGreen("{0} 更新成功".format(timer.simple_time()))
except Exception as e:
    printRed(e)
    printRed("{0} 更新失败，尝试前往 https://github.com/AJCheng726/AutoPlayer_WorldFlipper 手动更新".format(timer.simple_time()))
