# XEduLLM-tools

<iframe src="//player.bilibili.com/player.html?isOutside=true&aid=112994499431048&bvid=BV12tWsePEmA&cid=500001656107517&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 开发历史
[2024.8.20]
当前发布版本为`Windows`版本，支持`win7-win11`。
安装包双击安装，包含一个软件本体（`XEduLLM工具.exe`）和一个`env`文件夹。

待升级项：本地持久化一个`json`，记忆历史`api key`，用户选择完模型后，自动匹配，避免到处找。

## 源码说明
运行源码UI只需要基础的python环境即可，以验证`win`、`mac`。想要启动大模型对话，则需要下面的环境：
```
pip install xedu-python gradio requests
```
源码可以根据需要修改使用。

## 如何打包为exe
利用pyinstaller：`pip install pyinstaller`
```
pyinstaller -F -w your/python/file.py
```
- `-F`：生成独立exe文件；
- `-w`：不要启动黑框命令行。

## 软件许可
https://github.com/EasonQYS/XEduLLM-tools/blob/main/LICENSE

## 发版（release）
https://github.com/EasonQYS/XEduLLM-tools/releases
