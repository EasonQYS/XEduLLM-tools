import tkinter as tk
from tkinter import ttk
import subprocess
import webbrowser
import os
import socket
import ipaddress
from tkinter import messagebox
import pyperclip
# 创建主窗口
root = tk.Tk()
root.title("XEduLLM")
root.geometry("380x300")

process = None
# 子进程的命令和参数
#cmd = 'set PATH=%cd%\env;%PATH%'
cmd = r'set PATH=%cd%/env;%PATH% & python env/config.py'
#cmd = ['set', 'PATH=%cd%\env;%PATH%', '&' ,'python','env\config.py']
def get_local_ip():
    """
    获取本机IP地址
    """
    try:
        # 创建一个socket对象
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 不需要连接到一个特定的地址，只需要一个有效的IP即可
        s.connect(('8.8.8.8', 80))
        # 获取本地IP地址
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"获取本机IP时发生错误: {e}")
        return None
def open_web(*args):
    p5 = inputbox3.get() # port
    if p5 == '':
        p5 = 7860
    else:
        try:
            p5 = int(p5)
        except:
            p5 = 7860
    url = 'http://'+str(get_local_ip())+':'+str(p5)
    #print(url)
    webbrowser.open(url, new=2)
# 用于启动子进程的函数
def start_subprocess():
    global process
    # 将 stdout 和 stderr 重定向到 log.txt 文件
    with open('log.txt', 'w') as outfile:
        process = subprocess.Popen(cmd, stdout=outfile, stderr=outfile,shell=True)

# 用于终止子进程的函数
def stop_subprocess():
    global process
    if process:
        # 获取当前Entry的值，并转换为整数
        current_value = int(inputbox3.get())
        # 增加1
        new_value = current_value + 1
        # 将新的值设置回Entry组件
        inputbox3.delete(0, tk.END)  # 清空Entry
        inputbox3.insert(0, str(new_value))  # 插入新的值
        process.terminate()  # 发送终止信号
        process.wait()       # 等待进程终止
        process = None

# 定义退出程序的函数
def on_closing():
    stop_subprocess()
    root.destroy()
def copy_to_clipboard(url):
    pyperclip.copy(url)
    messagebox.showinfo("复制成功", "链接已复制到剪贴板")
def start():
    try:
        os.makedirs('env',exist_ok=True)
        with open('env/config.py','w',encoding='utf-8')as f:
            f.write('from XEdu.LLM import Client\n')
            p1 = optionbox1.get() #provider
            if p1 == '通义千问':
                p1='qwen'
            elif p1=='智谱清言':
                p1='glm'
            elif p1=='Kimi':
                p1='moonshot'
            elif p1=='深度求索':
                p1='deepseek'
            p2 = optionbox2.get() # model
            p3 = inputbox1.get() # api_key
            p4 = inputbox2.get() # prompt
            p5 = inputbox3.get() # port
            if p5 == '':
                p5 = 7860
            else:
                try:
                    p5 = int(p5)
                except:
                    p5 = 7860
                    
            f.write(f"chatbot = Client(provider='{p1}', model='{p2}', api_key='{p3}')\n")
            if p4 !='':
                f.write(f"chatbot.set_system('{p4}')\n")
            f.write(f"chatbot.run(host='0.0.0.0', port={p5})")
        run_window = tk.Toplevel(root)
        run_window.geometry("400x300")
        run_window.geometry(f'+{position_x+350}+{position_y}')
        run_window.title("帮助：如何使用")
        title = ttk.Label(run_window, text='服务已启动，服务地址为：')
        title.pack(pady=20)
        url = 'http://'+str(get_local_ip())+':'+str(p5)
        url_label = ttk.Label(run_window, text=url, cursor="hand2")
        url_label.bind("<Button-1>", lambda event: copy_to_clipboard(url))
        url_label.pack(pady=10)
        info = ttk.Label(run_window, text='可在浏览器体验，也可以发送该地址给学生使用（限局域网）。')
        info.pack(pady=10)
        prompt = ttk.Label(run_window, text='角色设定即提示词，例如“充当编程助手，禁止输出代码以外的任何内容。”')
        prompt.pack(pady=15)
        info2 = ttk.Label(run_window, text = '常见问题：端口占用。由于端口已被其他服务占用，请尝试其他4位数字。')
        info2.pack()
        info3 = ttk.Label(run_window, text = '常见问题：无法打开网址，检查填写信息。具体错误请参见log.txt。')
        info3.pack()
        info4 = ttk.Label(run_window, text="<<<<<<XEduLLM使用说明>>>>>>", cursor="hand2")
        info4.bind("<Button-1>", lambda event, url=url: webbrowser.open("https://xedu.readthedocs.io/zh-cn/master/xedu_llm.html", new=2))
        info4.pack(pady=20)
        start_subprocess()
    except Exception as e:
        # 捕获异常，并处理
        with open('log.txt', 'w') as log_file:  # 'a' 表示追加模式
            log_file.write(f"发生错误: {e}\n")  # 将错误信息写入log.txt文件
        print(f"错误已记录到log.txt: {e}")



# 设置窗口在屏幕中央
position_x = (root.winfo_screenwidth() - 700) // 2
position_y = (root.winfo_screenheight() - 300) // 2
root.geometry(f'+{position_x}+{position_y}')

title = tk.Label(root, text="XEduLLM大语言模型工具")
title.grid(row=0,column=1,pady=10)

# 在这里定义StringVar变量
var1 = tk.StringVar(root)
var2 = tk.StringVar(root)


provider_label = ttk.Label(root, text="服务商:")
provider_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
# 第一个选择框
optionbox1 = ttk.Combobox(root, textvariable=var1)
optionbox1['values'] = ('通义千问', 'openrouter', 'Kimi','深度求索','智谱清言')
optionbox1.set("请选择")  # 设置默认选项
optionbox1.grid(row=1, column=1, padx=5, pady=5)

model_label = ttk.Label(root, text="模型:")
model_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)

def update_second_optionbox(*args):
    if optionbox1.get() == '通义千问':
        optionbox2['values'] = ('qwen2-1.5b-instruct','qwen-turbo', 'qwen1.5-72b-chat', 'qwen1.5-1.8b-chat', 'codeqwen1.5-7b-chat', 'qwen-72b-chat',  'qwen-7b-chat',  'qwen2-7b-instruct', 'qwen2-0.5b-instruct', 'qwen2-57b-a14b-instruct')
    elif optionbox1.get() == 'openrouter':
        optionbox2['values'] = ('mistralai/mistral-7b-instruct:free', 'openai/chatgpt-4o-latest', 'meta-llama/llama-3.1-8b-instruct:free',  'qwen/qwen-2-7b-instruct:free', 'google/gemma-2-9b-it:free',  'microsoft/phi-3-medium-128k-instruct:free',  'meta-llama/llama-3-8b-instruct:free',  'google/gemma-7b-it:free',  'nousresearch/nous-capybara-7b:free', 'openchat/openchat-7b:free', 'undi95/toppy-m-7b:free', '...')
    elif optionbox1.get() == '智谱清言':
        optionbox2['values']= ('glm-4', 'glm-3-turbo')
    elif optionbox1.get() == 'Kimi':
        optionbox2['values']= ('moonshot-v1-8k','moonshot-v1-32k',  'moonshot-v1-128k')
    elif optionbox1.get() == '深度求索':
        optionbox2['values']= ('deepseek-chat', 'deepseek-coder')
    # 无论选择什么，都重置第二个选择框为“请选择”
    optionbox2.set(optionbox2['values'][0])
# 绑定第一个选择框的选项变化事件
optionbox1.bind('<<ComboboxSelected>>', update_second_optionbox)

# 第二个选择框
optionbox2 = ttk.Combobox(root, textvariable=var2)
optionbox2['values'] = ("请选择")
optionbox2.set("请选择")  # 设置默认选项
optionbox2.grid(row=2, column=1, padx=5, pady=5)

token_label = ttk.Label(root, text="API_Key:")
token_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)

inputbox1 = ttk.Entry(root, textvariable=tk.StringVar(root))
inputbox1.grid(row=3, column=1, padx=5, pady=5)

# 添加问号图标
question_mark = '?'  # 使用问号字符作为图标
question_icon = ttk.Label(root, text=question_mark, cursor="hand2")

question_icon.grid(row=3, column=2, padx=5, pady=5)

# 创建 ToolTip 功能
tooltip = None

def show_tooltip(event):
    global tooltip
    if tooltip is None:
        tooltip = tk.Toplevel(root)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+%d+%d" % (event.x_root + 20, event.y_root + 20))  # 根据需要调整位置
        tooltip_label = ttk.Label(tooltip, text="如何获取？", background="white")
        tooltip_label.pack()

def hide_tooltip(event):
    global tooltip
    if tooltip:
        tooltip.destroy()
        tooltip = None
def help_window(*args):
    h_window = tk.Toplevel(root)
    h_window.geometry("400x300")
    h_window.geometry(f'+{position_x+350}+{position_y}')
    h_window.title("帮助：如何获取API_Key")
    prov = ['通义千问', 'openrouter', 'Kimi','深度求索','智谱清言']
    urls = ["https://dashscope.console.aliyun.com/apiKey", "https://openrouter.ai/settings/keys", "https://platform.moonshot.cn/console/api-keys","https://platform.deepseek.com/api_keys","https://open.bigmodel.cn/usercenter/apikeys"]
    for i, url in enumerate(urls):
        name = ttk.Label(h_window, text=prov[i]+':')
        name.grid(row=i, column=0, sticky="e", padx=5, pady=5)
        label = ttk.Label(h_window, text=url, cursor="hand2")
        label.bind("<Button-1>", lambda event, url=url: webbrowser.open(url, new=2))
        label.grid(row=i, column=1, sticky="w", padx=5, pady=5)
    info = ttk.Label(h_window, text="您可点击上方链接注册并获取各平台API Key。")
    info.grid(row=6, column=1, sticky="w", padx=5, pady=5)
    info2 = ttk.Label(h_window, text="免费赠送额度通常就可以满足班级使用需求。")
    info2.grid(row=7, column=1, sticky="w", padx=5, pady=5)
    info3 = ttk.Label(h_window, text="<<<<<<XEduLLM使用说明>>>>>>", cursor="hand2")
    info3.bind("<Button-1>", lambda event, url=url: webbrowser.open("https://xedu.readthedocs.io/zh-cn/master/xedu_llm.html", new=2))
    info3.grid(row=8, column=1, sticky="w", padx=5, pady=5)
    
    
# 绑定鼠标悬停和离开事件
question_icon.bind('<Enter>', show_tooltip)
question_icon.bind('<Leave>', hide_tooltip)
question_icon.bind('<Button-1>', help_window)

promt_label = ttk.Label(root, text="角色设定（可留空）:")
promt_label.grid(row=4, column=0, sticky="e", padx=5, pady=5)

inputbox2 = ttk.Entry(root, textvariable=tk.StringVar(root))
inputbox2.grid(row=4, column=1, padx=5, pady=5)

port_label = ttk.Label(root, text="端口（默认7860）:")
port_label.grid(row=5, column=0, sticky="e", padx=5, pady=5)

inputbox3 = ttk.Entry(root, textvariable=tk.StringVar(root))
inputbox3.grid(row=5, column=1, padx=5, pady=5)
inputbox3.insert(0, '7860')  # 设置默认值

# 创建提交按钮
submit_button = tk.Button(root, text="启动服务", command=start)
submit_button.grid(row=6, column=0, padx=5, pady=5)

# 创建提交按钮
submit_button = tk.Button(root, text="停止服务", command=stop_subprocess)
submit_button.grid(row=6, column=1, padx=5, pady=5)

    
web_label = ttk.Label(root, text="<<<<<<点此打开网页>>>>>>", cursor="hand2")
web_label.grid(row=7, column=1, sticky="e", padx=5, pady=5)
web_label.bind('<Button-1>', open_web)

# 绑定关闭窗口事件
root.protocol("WM_DELETE_WINDOW", on_closing)

# 启动事件循环
root.mainloop()