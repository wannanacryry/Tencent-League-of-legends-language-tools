from tkinter import filedialog
import tkinter as tk
import os
from pathlib import Path
import tkinter.messagebox
import sys

def files_exist(file):
    p = Path(file)
    path_exists = p.exists()
    return path_exists

def select_folder():
    LOL_PATH = ""
    askdirectory = tk.Tk()
    askdirectory.withdraw()  # 隐藏根窗口
    folder_path = filedialog.askdirectory()  # 弹出对话框让用户选择文件夹
    if os.path.normpath(folder_path) != None:
        LOL_PATH = os.path.normpath(folder_path)
    Language_Files_1 = LOL_PATH + "\\LeagueClient\\system.yaml"
    print (f"sssss{LOL_PATH}")
    if not folder_path:
        sys.exit()
    else:

        # 这里可以添加处理文件夹路径的代码
        askdirectory.destroy()  # 处理完毕后关闭程序
    print('选择的文件夹路径:', folder_path)
    print(files_exist(os.path.normpath(folder_path + Language_Files_1)))
    if files_exist(os.path.normpath( Language_Files_1)) == True:
        return folder_path
    else:
        tkinter.messagebox.showwarning(title = '',message='选择有误，请选择游戏根目录。')
        return select_folder()