PyInstaller安装

1. 使用：pip install PyInstaller

2. 去官方网站 http://www.pyinstaller.org/ 下载最新版,解压到本地目录

 

pyinstaller 是可以用在linux和windows系统。不能和 tkinter 等库，打包成单独一个文件

 

使用方法

　　使用命令：pyinstaller -F -w -i icon.ico test.py

　　执行后，打包好的可执行文件默认放在dist目录，打开dist就能看到test.exe

参数:

-F 打包成单独的文件

-D 打包成一个目录

-w 就是窗口程序

-d debug程序

-c 命令行程序

–i FILE.ICO 程序图标