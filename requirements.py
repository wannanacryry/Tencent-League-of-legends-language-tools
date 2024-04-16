import re
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox
import shutil
import os
from pathlib import Path
import subprocess
from tkinter import filedialog
import main


locale = {"ar_SA":["Arabic","Arabic (Saudi Arabia)"],"bn_BD":["Bangla","Bangla (Bangladesh)"],"bn_IN":["Bangla","Bangla (India)"],"cs_CZ":["Czech","Czech (Czech Republic)"],"da_DK":["Danish","Danish (Denmark)"],"de_AT":["German","Austrian German"],"de_CH":["German","Swiss" "German"],"de_DE":["German","Standard German (as spoken in Germany)"],"el_GR":["Greek","Modern Greek"],"en_AU":["English","Australian English"],"en_CA":["English","Canadian English"],"en_GB":["English","British English"],"en_IE":["English","Irish English"],"en_IN":["English","Indian English"],"en_NZ":["English","New Zealand English"],"en_US":["English","US English"],"en_ZA":["English","English (South Africa)"],"es_AR":["Spanish","Argentine Spanish"],"es_CL":["Spanish","Chilean Spanish"],"es_CO":["Spanish","Colombian Spanish"],"es_ES":["Spanish","Castilian Spanish (as spoken in Central-Northern Spain)"],"es_MX":["Spanish","Mexican Spanish"],"es_US":["Spanish","American Spanish"],"fi_FI":["Finnish","Finnish (Finland)"],"fr_BE":["French","Belgian French"],"fr_CA":["French","Canadian French"],"fr_CH":["French","Swiss French"],"fr_FR":["French","Standard French (especially in France)"],"he_IL":["Hebrew","Hebrew (Israel)"],"hi_IN":["Hindi","Hindi (India)"],"hu_HU":["Hungarian","Hungarian (Hungary)"],"id_ID":["Indonesian","Indonesian (Indonesia)"],"it_CH":["Italian","Swiss Italian"],"it_IT":["Italian","Standard Italian (as spoken in Italy)"],"ja_JP":["Japanese","Japanese (Japan)"],"ko_KR":["Korean","Korean (Republic of Korea)"],"nl_BE":["Dutch","Belgian Dutch"],"nl_NL":["Dutch","Standard Dutch (as spoken in The Netherlands)"],"no_NO":["Norwegian","Norwegian (Norway)"],"pl_PL":["Polish","Polish (Poland)"],"pt_BR":["Portugese","Brazilian Portuguese"],"pt_PT":["Portugese","European Portuguese (as written and spoken in Portugal)"],"ro_RO":["Romanian","Romanian (Romania)"],"ru_RU":["Russian","Russian (Russian Federation)"],"sk_SK":["Slovak","Slovak (Slovakia)"],"sv_SE":["Swedish","Swedish (Sweden)"],"ta_IN":["Tamil","Indian Tamil"],"ta_LK":["Tamil","Sri Lankan Tamil"],"th_TH":["Thai","Thai (Thailand)"],"tr_TR":["Turkish","Turkish (Turkey)"],"zh_CN":["Chinese","Mainland China, simplified characters"],"zh_HK":["Chinese","Hong Kong, traditional characters"],"zh_TW":["Chinese","Taiwan, traditional characters"]}

LOL_PATH = main.select_folder()
Language_Files_1 = LOL_PATH + "\\LeagueClient\\system.yaml"
Language_Files_2 = LOL_PATH + "\\Riot Client\\system.yaml"
Language_Files_3 = LOL_PATH + "\\Riot Client Data\\User Data\\Config\\RiotClientSettings.yaml"
Language_Files_4 = LOL_PATH + "\\LeagueClient\\Config\\LeagueClientSettings.yaml"
Language_Files_5 = LOL_PATH + "\\Game\\DATA\\FINAL"
 # LOL的路径
LOL_NAME = "LeagueClient.exe" # LOL的进程名
RIOT_NAME = "RiotClientServices.exe" # Riot的进程名
TCLS_PATH = LOL_PATH + "\\TCLS\\client.exe"
Old_Language = None


New_Language = None


def region_avabile():
    localelist = list(locale.keys())
    avabile_region = []
    for region in localelist :
        locale_filename = f"UI.{region}.wad.client"
        print (Language_Files_5 + "\\" + locale_filename)
        temp = files_exist (Language_Files_5 + "\\" + locale_filename)
        if temp == True :
            avabile_region.append (region)
        else:
            continue
    return avabile_region

def openexe():
    subprocess.Popen (TCLS_PATH)


def languageold (LeagueClient,Riot_Client,Riot_Client_Data):
    """
    用于判断目前的语言文件是否存在问题
    :param LegueClienta:LeagueClient 语言代码
    :param Riot_Client: Riot_Client 语言代码
    :param Riot_Client_Data: Riot_Client_Data 语言代码
    :return: 如果三者一致，返回pass并直接修改全局变量Old_Language = pass；三者不一致，返回error 不修改全局变量Old_Language
    """
    global Old_Language
    if LeagueClient == Riot_Client and Riot_Client == Riot_Client_Data:
        Old_Language = LeagueClient

        return "pass"

    else:
        return "error"


def LeagueClientSettings_change (content,New_Language,mode):
    if mode == "r":
        language = re.findall(r'locale: .\w\w_[A-Z]{2}.',content)
        language = str(language[0])[-6:-1]
        return language
    else:
        tempNew_Language = New_Language + "\""
        content = re.sub(r'(?<=locale: ").*', tempNew_Language, content)
        return content

def LeagueClient_change(content,New_Language,mode):
    """

    :param content: "\\LeagueClient\\system.yaml"的打开文件内容
    :param New_Language: 需要修改的新语言，可以使用全局变量传参
    :param mode: "r" 为读取现有文件内容，但是不会修改文件。默认空会修改文件
    :return: 'r'模式下 返回语言代码；非r模式返回修改新语言后的文件打开内容和语言，非'r'模式为空
    """
    if mode == "r":
        language = re.findall(r'default_locale: \w\w_[A-Z]{2}',content)
        language = str(language[0])[-5:]
        return language
    else:
        content = re.sub(r'(?<=default_locale: ).*', New_Language, content)
        return content


def Riot_Client_change(content,New_Language,mode):
    if mode == "r":
        language1 = re.findall(r'locale=......?.?.?',content)
        print (str(language1[0]))
        if "{locale}" not in str(language1[0]) :
            language1 = str(language1[0])[-5:]
        else:
            language1 = str(language1[0])[-8:]


        language2 = re.findall(r'    default_locale: \w\w_[A-Z]{2}',content)
        language2 = str(language2[0])[-5:]
        return language1,language2
    else:
        content = re.sub(r'(?<=  - --locale=).*', New_Language, content)
        content = re.sub(r'(?<=    default_locale: ).*', New_Language, content)
        return content

def Riot_Client_Data_changer(content,New_Language,mode):
    if mode == "r":
        language1 = re.findall(r'locale: \"\w\w\_[A-Z]{2}\"',content)
        language1 = str(language1[0])[-6:-1]

        return language1
    else:
        tempNew_Language = New_Language + "\""
        content = re.sub(r'(?<=        locale: ").*', tempNew_Language, content)
        return content


def open_ymal (file_path):
    """
    :param file_path: 文件路径
    :return: pythonopen类型文件表格
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def change_file_info_and_save (content,file_path):
    '''
    :param content: pythonopen类型文件表格
    :return: 无
    '''
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def button_function_test ():
    d = LeagueClient_change(content=open_ymal(Language_Files_1), New_Language=New_Language, mode="r")
    e, f = Riot_Client_change(content=open_ymal(Language_Files_2), New_Language=New_Language, mode="r")
    c = Riot_Client_Data_changer(content=open_ymal(Language_Files_3), New_Language=New_Language, mode="r")
    if languageold(c, d, f) == "pass":
        Entry_lollangstats.delete(first = 0,last = 999)
        Entry_lollangstats.insert(tk.END, f"目前的语言是{Old_Language}")

def files_exist(file):
    p = Path(file)
    path_exists = p.exists()
    return path_exists

def files_backup (source_file,dest_file):
    shutil.copy2 (source_file,dest_file)


def button_function_change ():

    if New_Language == None or New_Language == " ":
        result = tkinter.messagebox.showwarning(title='', message='什么都没做，因为你没选择任何语言。')
    else:
        change_file_info_and_save(content = LeagueClient_change(mode = "w",content = open_ymal(Language_Files_1),New_Language = New_Language),file_path = Language_Files_1 )
        change_file_info_and_save(content = Riot_Client_change(mode = "w",content = open_ymal(Language_Files_2),New_Language = New_Language),file_path = Language_Files_2 )
        change_file_info_and_save(content = Riot_Client_Data_changer(mode = "w",content = open_ymal(Language_Files_3),New_Language = New_Language),file_path = Language_Files_3 )
        change_file_info_and_save(
            content=LeagueClientSettings_change(mode="w", content=open_ymal(Language_Files_4), New_Language=New_Language),
            file_path=Language_Files_4)
        result = tkinter.messagebox.showwarning(title = '',message='修改完毕。')





#change_file_info_and_save(content = LeagueClient_change(content = open_ymal(Language_Files_1),New_Language = New_Language),file_path = Language_Files_1 )
#change_file_info_and_save(content = Riot_Client_change(content = open_ymal(Language_Files_2),New_Language = New_Language),file_path = Language_Files_2 )
#change_file_info_and_save(content = Riot_Client_Data_changer(content = open_ymal(Language_Files_3),New_Language = New_Language),file_path = Language_Files_3 )
#打开软件后获取现在的语言信息
d = LeagueClient_change(content = open_ymal(Language_Files_1),New_Language = New_Language,mode = "r")
e,f = Riot_Client_change(content = open_ymal(Language_Files_2),New_Language = New_Language,mode = "r")
c = Riot_Client_Data_changer(content = open_ymal(Language_Files_3),New_Language = New_Language,mode = "r")
print (c,d,e,f)
print (languageold (c,d,f))
print (Old_Language)

##第一次打开备份现有的文件，如果存在备份即不再备份
if files_exist(os.path.dirname(Language_Files_1) + "\\system.yaml.bak") == False:
    print(files_exist(os.path.dirname(Language_Files_1) + "\\system.yaml.bak"))
    files_backup(Language_Files_1, os.path.dirname(Language_Files_1) + "\\system.yaml.bak")

if files_exist(os.path.dirname(Language_Files_2) + "\\system.yaml.bak") == False:
    print(files_exist(os.path.dirname(Language_Files_2) + "\\system.yaml.bak"))
    files_backup(Language_Files_2, os.path.dirname(Language_Files_2) + "\\system.yaml.bak")

if files_exist(os.path.dirname(Language_Files_3) + "\\RiotClientSettings.yaml.bak") == False:
    print(files_exist(os.path.dirname(Language_Files_3) + "\\RiotClientSettings.yaml.bak"))
    files_backup(Language_Files_3, os.path.dirname(Language_Files_3) + "\\RiotClientSettings.yaml.bak")

if files_exist(os.path.dirname(Language_Files_4) + "\\LeagueClientSettings.yaml.bak") == False:
    print(files_exist(os.path.dirname(Language_Files_4) + "\\LeagueClientSettings.yaml.bak"))
    files_backup(Language_Files_4, os.path.dirname(Language_Files_4) + "\\LeagueClientSettings.yaml.bak")


print (region_avabile())
##主窗口
windows = tk.Tk()
windows.title("Language Tools")
windows.geometry("400x200")

#信息框
info_message = tk.Message(windows,text = f"检测客户端文件后发现，以下地区可以使用：\n{region_avabile()}",width = 300,)
info_message.pack()
info_message.place(x=70, y=130)
Language_info_message = tk.Message(windows,text = f"目前区域是{Old_Language},请选择一个语言",width = 300)
Language_info_message.pack()
Language_info_message.place(x=96, y=1)


#下拉选单
def combo_box_select (event):
    """
    :param event: 监测下拉框被修改
    :return: 修改全局变量 New_Language
    """
    global New_Language
    selected_option = combo_box.get()
    New_Language = selected_option
    Language_info_message.config(text=locale.get(selected_option))

print (list(region_avabile()))
combo_box_values = list(region_avabile())
combo_box_values.append(" ")
combo_box = ttk.Combobox(windows, values=combo_box_values)

if Old_Language in combo_box_values:
    combo_box.current(combo_box_values.index(Old_Language))  # 设置默认选择为第一个选项
else:
    combo_box.current(combo_box_values.index(" "))
combo_box.pack()
combo_box.place (x=110 ,y = 25)
#下拉菜单修改事件检测
combo_box.bind ("<<ComboboxSelected>>",combo_box_select)


#按钮
button_change = tk.Button (text = "修改",command = button_function_change)
button_change.pack()
button_change.place(x=175,y=60)
button_start_tcls = tk.Button (text = "开始TCLS",command = openexe)
button_start_tcls.pack()
button_start_tcls.place(x=160,y=95)
windows.mainloop()






