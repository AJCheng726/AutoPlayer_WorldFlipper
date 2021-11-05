# 0为adb模式，通过USB或无线连接手机/模拟器，使用adb命令截图和模拟点击
# 1为桌面模式，在电脑桌面运行PC客户端/模拟器，PIL截屏和pyautogui操作鼠标点击
mode = 0
#图片匹配精确度，0-1之间，默认0.85无需修改，如果匹配出错误目标则提高精度，如果要模糊匹配则降低精度
accuracy = 0.8
#匹配目标图片地址， 默认在./wanted文件夹
wanted_path = './wanted' 
# 蹭房设备号
main_device = 'emulator-5556' 
# 建房设备号
sub_device = 'emulator-5554' 
# 模拟器宽高
device_w,device_h = 540,960
# 截图间隔时间，用于所有wait函数
screenshot_blank = 0.5


