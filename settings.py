# 0为adb模式，通过USB或无线连接手机/模拟器，使用adb命令截图和模拟点击
# 1为桌面模式，在电脑桌面运行PC客户端/模拟器，PIL截屏和pyautogui操作鼠标点击
mode = 0
# debug模式，开启则打印所有操作
debug = False
# 图片匹配精确度，0-1之间，默认0.85无需修改，如果匹配出错误目标则提高精度，如果要模糊匹配则降低精度
accuracy = 0.7
# 匹配目标图片地址， 默认在./wanted文件夹
wanted_path = "./wanted"
# 模拟器宽高，直接把模拟器改成和下面一样的，别改这个参数
device_w, device_h = 540, 960
# 截图间隔时间，用于所有wait函数，如果CPU占用太高就调久一点
screenshot_blank = 0.5
# adb路径
adb_path = "toolkits\\ADB\\adb.exe"

# 超时，超时则认为阵亡或房间解散
timeout = 300

# 蹭房设备号，如果是雷电64单开就填emulator-5554
canzhan_device_1 = "emulator-5556"
canzhan_device_2 = "emulator-5560"
# 建房设备号，如果是雷电64多开，就按多开每次递增2
fangzhu_device = "emulator-5554"
# 房主ID用哪个，模拟器原比例截图放到wanted文件夹下，名字填在下面
fangzhu_account = "azhecheng"

# 房主退出后等待多少秒再重建
wait_outof_room = 0

# 重复刷本设备号
loop_device = "emulator-5556"



