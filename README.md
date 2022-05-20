# AutoPlayer_WorldFlipper
<p align="center">
  <img src="https://user-images.githubusercontent.com/31361978/158060158-3edf56cb-5daf-435c-8504-740d4c0a3b09.png"/>
  <img src="https://user-images.githubusercontent.com/31361978/164265458-58422bf9-d372-4538-b787-609f01f2d484.png"/>
</p>

带GUI的世界弹射物语国服脚本，支持稳定3开灵车、做每日任务（搬玛那商店、打4次迷宫、自建3次共斗）

仅支持540x960分辨率，推荐使用夜神模拟器64位，B服需要覆盖Release中的替换包

第一次使用（前往 https://github.com/AJCheng726/AutoPlayer_WorldFlipper/releases/ ）下载Release版（解压失败的话尝试bandzip），包含了脚本所需的Python和ADB环境，后续可增量覆盖toolkits以外的部分

有问题可加群，985729887（回答github即可），欢迎加好友一起挂共斗

## 使用说明
ApWF.exe启动界面，如果被杀毒软件误删使用gui.bat也可

### 准备工作

1、（必要）将模拟器的分辨率改为540x960

2、设置编队：主页打开teamset.ini设置打本编队，格式为SET-TEAM，如果为空则不改变队伍。

![image](https://user-images.githubusercontent.com/31361978/164265744-990f3177-e22f-444f-92ff-c3415596179a.png)  ![image](https://user-images.githubusercontent.com/31361978/164270528-a378295a-eb5b-42b1-a3fe-15c80c34ae8d.png)

注意房主和参战共用同一编队配置，如果大小号编队不一致，建议建立ApWF副本使用全新的编队配置

2、在模拟器主页即可点击GO!，随后自动登录游戏开始对应子进程

### 单人日常

点击GO!后会自动完成：清空玛那商店→打4次每日迷宫→按房主页配置建3次共斗→前往主页

![image](https://user-images.githubusercontent.com/31361978/158062148-51cd0860-94be-4e5f-824b-7d040ae86bee.png)

支持的迷宫选项在wanted文件夹下maze开头的图片

![image](https://user-images.githubusercontent.com/31361978/158062302-088ab8cb-03e8-4ec6-a000-0fa837f6e28d.png)

### 多开共斗

![image](https://user-images.githubusercontent.com/31361978/158063048-041c8c8e-a828-4cde-9340-dfdaadd882f5.png)

#### 房主页配置：

1、房主设备：建房号所用的模拟器设备号。每个模拟器连接adb的方法不同，自行搜索并配合工具箱中的[[查询所有设备]]获取。

2、最小玩家数：共斗人数下限。房间人数达到后房主点挑战，支持2 or 3。

3、随机招募：为0时关闭随机招募仅双向关注可看到房间，为1开启单向关注和随机招募。

4、活动模式：0时为日常模式,1时打活动模式。

> 日常模式参数：

> 4.1、Raid难度：建房时选择的难度，1代表从上到下的第一个（超级或者高），2代表从上到下第二个（高级或者高+），以此类推。

> 4.2、日常目标：支持的boss搜索wanted文件夹下raid_开头的图片。

> 活动模式参数：

> 4.3、活动目标：当期活动boss，一般为raid_event_h+或raid_event_s，代表高+和超级本。

#### 参战页配置：

1、参战1、参战2设备：参战使用的模拟器设备号，获取方法同房主配置1.

2、房主截图：默认配置为icon_chufaqian,icon_chufaqianpickup，此配置下见房就进。如果需要指定进小号房，可截图小号房名放到wanted文件夹（截图使用工具箱内的截图功能，在screen找到截图后裁剪，截图范围示例如下），多个小号可用英文逗号隔开，每次更新覆盖前记得保留好自己的小号截图。

![image](https://user-images.githubusercontent.com/31361978/169441610-18758d62-ee81-4c7b-aac8-7d81f224fadd.png)![image](https://user-images.githubusercontent.com/31361978/169441488-9bb9d150-3d08-43e5-86c4-fa86cf5c2fbd.png)

### 常见QA

1、如何排除是不是模拟器的问题？

自行连接adb后，如果查询结果如下，则排除是模拟器的问题

![image](https://user-images.githubusercontent.com/31361978/158061465-d39b19b7-5821-465a-8a36-c41b194da83a.png)

&ensp;1.1 蓝叠模拟器参考 https://www.cnblogs.com/rogunt/p/13047394.html 连接ADB

&ensp;1.2 夜神模拟器使用工具箱中的“连接夜神设备”，自动连接ADB
