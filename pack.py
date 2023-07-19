
import subprocess

def package_script(script_file):
    # 构建打包命令
    command = f'pyinstaller --noconsole --onefile {script_file}'

    # 执行打包命令，并捕获输出信息
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,encoding='cp932', errors='ignore')

    # 实时显示打包进度信息
    for line in process.stdout:
        print(line.strip())

    # 等待打包命令完成
    process.wait()

    # 检查打包是否成功
    if process.returncode == 0:
        print("打包完成！")
    else:
        print("打包失败！")

# 替换为您要打包的脚本文件名
script_file = "split_tool.py"

# 调用打包函数
package_script(script_file)