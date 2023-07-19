import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import subprocess
import os
import configparser
import re
import sys
# Get the current directory
current_directory = os.getcwd()

# Set the log file path in the current directory
log_file_path = os.path.join(current_directory, "log.txt")

# Redirect stdout to the log file with UTF-8 encoding
sys.stdout = open(log_file_path, "w", encoding="utf-8")

# 创建配置文件对象
config = configparser.ConfigParser()

# 初始化默认时间
default_start_min = "00"
default_start_sec = "00"
default_end_min = "01"
default_end_sec = "00"

# 读取配置文件
config.read("config.ini")
if "DEFAULT" in config:
    default_start_min = config["DEFAULT"].get("start_min", default_start_min)
    default_start_sec = config["DEFAULT"].get("start_sec", default_start_sec)
    default_end_min = config["DEFAULT"].get("end_min", default_end_min)
    default_end_sec = config["DEFAULT"].get("end_sec", default_end_sec)

def save_config():
    # 创建配置文件的 DEFAULT 部分
    config["DEFAULT"] = {
        "start_min": start_min_combobox.get(),
        "start_sec": start_sec_combobox.get(),
        "end_min": end_min_combobox.get(),
        "end_sec": end_sec_combobox.get()
    }

    # 将配置写入文件
    with open("config.ini", "w") as config_file:
        config.write(config_file)

def convert_to_mp3(file_path):
    try:
        # Conversion code here
        print("Starting MP3 conversion...")
        # Your conversion logic goes here
        print("开始转换为 MP3 格式...")
        output_dir = os.path.dirname(file_path)  # 与 MP4 文件相同的目录路径
        output_file = os.path.splitext(file_path)[0] + ".mp3"
        mp3_cmd = f'ffmpeg -y -i "{file_path}" -vn -acodec mp3 -ab 256k "{output_file}"'
        subprocess.call(mp3_cmd, shell=True)
        print("MP3 转换完成！")
        # 删除原始的 MP4 文件
        os.remove(file_path)
        print("原始 MP4 文件已删除！")
        # Display success message
        messagebox.showinfo("Success", "MP3 conversion completed!")
    except Exception as e:
        # Display error message
        messagebox.showerror("Error", f"MP3 conversion failed: {str(e)}")



def split_video():
    file_path = filedialog.askopenfilename()
    if file_path:
        start_min = start_min_combobox.get()
        start_sec = start_sec_combobox.get()
        end_min = end_min_combobox.get()
        end_sec = end_sec_combobox.get()

        # 根据选择的分钟和秒钟计算时间值
        start_time = f"00:{start_min.zfill(2)}:{start_sec.zfill(2)}"
        end_time = f"00:{end_min.zfill(2)}:{end_sec.zfill(2)}"

         # 获取输入文件的基本名称（不包含路径和后缀）
        input_file_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # 去除输入文件名中小括号及其内容
        input_file_name = re.sub(r'\(.*\)', '', input_file_name).strip()
        # 分割为MP4格式
        output_file_mp4 = f"{input_file_name}_{start_min}m{start_sec}s-{end_min}m{end_sec}s.mp4"
        output_file_mp4 = os.path.join("output", output_file_mp4)
        mp4_cmd = f'ffmpeg -y -i "{file_path}" -ss {start_time} -to {end_time} -c copy "{output_file_mp4}"'
        subprocess.run(mp4_cmd, shell=True)
        print("MP4 视频分割完成！")

        # 转换为MP3格式
        convert_to_mp3(output_file_mp4)
    else:
        print("未选择任何文件。")

def on_closing():
    # 保存配置
    save_config()
    window.destroy()

# 创建主窗口
window = tk.Tk()
window.geometry("600x800")  # 设置窗口大小为 400x250

# 创建分割开始分钟标签和下拉菜单
start_min_label = tk.Label(window, text="开始分钟：")
start_min_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
start_min_combobox = ttk.Combobox(window, values=[str(i).zfill(2) for i in range(60)])  # 00-59分钟
start_min_combobox.set(default_start_min)  # 设置默认选择为上次选择的分钟
start_min_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# 创建分割开始秒钟标签和下拉菜单
start_sec_label = tk.Label(window, text="开始秒钟：")
start_sec_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")
start_sec_combobox = ttk.Combobox(window, values=[str(i).zfill(2) for i in range(60)])  # 00-59秒
start_sec_combobox.set(default_start_sec)  # 设置默认选择为上次选择的秒钟
start_sec_combobox.grid(row=0, column=3, padx=10, pady=5, sticky="w")

# 创建分割结束分钟下拉菜单
end_min_label = tk.Label(window, text="结束分钟：")
end_min_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
end_min_combobox = ttk.Combobox(window, values=[str(i).zfill(2) for i in range(60)])  # 00-59分钟
end_min_combobox.set(default_end_min)  # 设置默认选择为上次选择的分钟
end_min_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# 创建分割结束秒钟下拉菜单
end_sec_label = tk.Label(window, text="结束秒钟：")
end_sec_label.grid(row=1, column=2, padx=10, pady=5, sticky="e")
end_sec_combobox = ttk.Combobox(window, values=[str(i).zfill(2) for i in range(60)])  # 00-59秒
end_sec_combobox.set(default_end_sec)  # 设置默认选择为上次选择的秒钟
end_sec_combobox.grid(row=1, column=3, padx=10, pady=5, sticky="w")

# 创建文件选择按钮
button = tk.Button(window, text="选择视频文件", command=split_video)
button.grid(row=2, column=0, columnspan=4, padx=10, pady=5)

# 注册关闭窗口的事件处理函数
window.protocol("WM_DELETE_WINDOW", on_closing)

# 运行主循环
window.mainloop()



