 Author: Dengwenbin 00190167 aka Arthur

 Date  : 2018-1-10 14:43:22

Description: 

##Part1: 移植说明：

1， 体验请使用已经编译好的apk安装到Android平板设备上（app提供模拟器支持。

2， 要求8寸安卓平板电脑，系统需要 Android 3.0 （Honeycomb）或者更高版本。

3， server.py 和 roscore 运行在 master 节点上。

4， server.py 提供 TF throttle 和 clock throttle。app可以通过控制server.py功能start或stop
    server.py 提供 网格(mesh) 和 纹理(texture) ,这些将被 markers 和 URDF 使用。
	server.py 要求 python版本 >= 2.6.5
	master节点需要安装TF throttle节点。
	
5， 预编译的应用兼容ARMv5TE指令集


6， 项目基于ROSJava，https://github.com/rosjava。
    需要其Android LIb支持https://github.com/rosjava/android_core

7， rviz.app是基础Android版本。使用rosjava在google code的陈旧归档代码:(需要进一步porting
    https://code.google.com/p/rosjava/source/detail?r=e51b1dd6b23f3f22892506960cfd0f4e3addbd05

8， 该版本基于NDK对libtiff做了进一步封装。用来加载tiff图像。

9， 编译请使用android studio，基于gradle进行编译。


##Part2: 模拟器

1，工具： virtualbox，[android-x86-6.0-r3.iso](http://www.android-x86.org/download)

2, 虚拟机选择桥接模式，以便android和master通信

3，效果图如下
   
   ![demo](https://github.com/GitBubble/rviz_android_porting/blob/master/assets/snapshot.PNG?raw=true)
   
## todo:
    
1, compile guide to be add

2, porting guide to be add

3, adapt to new rosjava to be added

4, simulation envronment to be added
