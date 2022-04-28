# AutoPlayer_WorldFlipper
<p align="center">
  <img src="https://user-images.githubusercontent.com/31361978/158060158-3edf56cb-5daf-435c-8504-740d4c0a3b09.png"/>
  <img src="https://user-images.githubusercontent.com/31361978/164265458-58422bf9-d372-4538-b787-609f01f2d484.png"/>
</p>

带GUI的世界弹射物语国服脚本，支持稳定3开灵车、做每日任务（搬玛那商店、打4次迷宫），目前已更新至半周年版本

仅支持540x960分辨率，推荐使用夜神模拟器64位，B服需要覆盖Release中的替换包

第一次使用（前往 https://github.com/AJCheng726/AutoPlayer_WorldFlipper/releases/ ）下载Release版（解压失败的话尝试bandzip），包含了脚本所需的Python和ADB环境，后续可增量覆盖toolkits以外的部分

有问题可加群，985729887（验证问题答案：540x960），欢迎加好友一起挂共斗

## 使用说明
gui.bat或ApWF.exe启动界面

### 准备工作

以下都是必要步骤：

1、将模拟器的分辨率改为540x960

2、使用工具箱中的查询所有设备确认模拟器启动且开启了adb调试

![image](https://user-images.githubusercontent.com/31361978/158061465-d39b19b7-5821-465a-8a36-c41b194da83a.png)

&ensp;2.1 蓝叠模拟器参考 https://www.cnblogs.com/rogunt/p/13047394.html 连接ADB

&ensp;2.2 夜神模拟器使用工具箱中的“连接夜神设备”，自动连接ADB

3、在模拟器主页即可点击GO!，随后自动登录游戏开始任务

### 设置编队

![image](https://user-images.githubusercontent.com/31361978/164265744-990f3177-e22f-444f-92ff-c3415596179a.png)  ![image](https://user-images.githubusercontent.com/31361978/164270528-a378295a-eb5b-42b1-a3fe-15c80c34ae8d.png)

主页打开teamset.ini设置打本编队，格式为SET-TEAM，如果为空则不改变队伍

注意房主和参战共用同一编队配置，如果大小号编队不一致，建议建立ApWF副本使用全新的编队配置

### 单人日常

点击GO!后会自动完成：清空玛那商店→打4次每日迷宫→按房主页配置建3次共斗→前往主页

![image](https://user-images.githubusercontent.com/31361978/158062148-51cd0860-94be-4e5f-824b-7d040ae86bee.png)

支持的迷宫选项在wanted文件夹下maze开头的图片

![image](https://user-images.githubusercontent.com/31361978/158062302-088ab8cb-03e8-4ec6-a000-0fa837f6e28d.png)

### 小号多开

![image](https://user-images.githubusercontent.com/31361978/158063048-041c8c8e-a828-4cde-9340-dfdaadd882f5.png)

#### 房主需要注意的参数：

1、房主设备：建房号所用的模拟器设备号，获取方法详见准备工作-2

2、最小玩家数：房间人数达到后房主点挑战，支持2、3

3、随机招募：为0时关闭随机招募仅双向关注可看到房间，为1开启单向关注和随机招募

4、活动模式：为0时打日常boss,为1时打活动boss，搭配下面的两个目标参数使用

5、Raid难度：建房时选择的难度，1-从上到下的第一个（超级或者高），2-从上到下第二个（高级或者高+），以此类推

6、活动目标：活动模式为1时生效，示例参考wanted文件夹下event_开头的图片,每次出新活动需要向wanted文件夹添加event_开头的图片

7、日常目标：活动模式为0时生效，支持的boss搜索wanted文件夹下raid_开头的图片

#### 参战需要注意的参数：

1、参战1、参战2设备：参战号所在的模拟器设备，获取方法详见准备工作-2

2、房主截图：默认见房就进，如果需要指定进小号房，可截图小号房名放到wanted文件夹，多个小号可用英文逗号隔开

### 活动

其他操作与多开共斗一样，注意修改活动模式参数，更新活动时替换wanted文件夹下的button_event.png
