import os
import sys
import subprocess

sys.path.append("./utils/")
sys.path.append("./")
from utils.print_color import *


def connect_to_nox(adb_path):
    tasklist = os.popen("tasklist | findstr NoxVMHandle.exe").read()
    pids = [x for x in tasklist.split()[1::6]]
    for pid in pids:
        addrport = os.popen("netstat -ano |findstr {0}".format(pid)).read().split()
        addrport = list(filter(lambda x: x.find(":") >= 0, addrport))
        port = [x.split(":")[1] for x in addrport]
        port = list(filter(lambda x: x[:2:] == "62", port))[0]
        out = os.popen("{0} connect 127.0.0.1:{1}".format(adb_path, port)).read().strip()
        printDarkPink(' '.join([out,port]))



if __name__ == "__main__":
    # connect_to_nox(adb_path="toolkits\\ADB\\adb.exe")
    pass