# ==========全局设置==========
# debug模式，开启则打印所有操作
debug = 0
# 图片匹配精确度，0-1之间，默认0.85无需修改，如果匹配出错误目标则提高精度，如果要模糊匹配则降低精度
accuracy = 0.75
# 匹配目标图片地址， 默认在./wanted文件夹
wanted_path = "./wanted"
# 模拟器宽高，直接把模拟器改成和下面一样的，别改这个参数
device_w, device_h = 540, 960
# 截图间隔时间，用于所有wait函数，如果CPU占用太高就调久一点
screenshot_blank = 0.5
# adb路径
adb_path = "toolkits\\ADB\\adb.exe"

# ==========弹射设置==========
# 弹射APK的包名和active类名,一般不用改
wf_apk_name,wf_active_class_name = 'com.leiting.wf','air.com.leiting.wf.AppEntry'
# ===单开/双开/三开刷共斗===
# 蹭房设备号，如果是雷电64单开就填emulator-5554
canzhan_device_1 = "emulator-5554"
canzhan_device_2 = "emulator-5560"
# 建房设备号，如果是雷电64多开，就按多开每次递增2
fangzhu_device = "emulator-5556"
# 房主ID用哪个，模拟器原比例截图放到wanted文件夹下，名字填在下面，按优先级从高到低找房
fangzhu_account = ["ajcheng_pickup","ajcheng","azhecheng_pickup","azhecheng"]
# 房间人数最小限制，已实现未测试
limit_player = 2
# 超时，超过则认为阵亡或房间解散
timeout = 600
battle_timeout = 300
# ===活动模式====
event_mode = 0
event_screenshot = "raid_event1"
# ===日常模式====
raid_choose = "raid_dashe"
# raid_choose = "raid_pickup"
# ===单机连战===
# 单人连战设备号
loop_device = "emulator-5554"




