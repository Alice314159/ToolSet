#本程序仅供内部测试使用
#请仔细核对数据内容
#本人不对数据真实有效性负责！
from tkinter import filedialog
import tkinter as tk
import os
import zipfile
from readPages import *
import shutil

import pkg_resources

installed_packages = [(d.project_name, d.version) for d in pkg_resources.working_set]
installed_packages.sort()

for package, version in installed_packages:
    print(f"{package} - {version}")

#选择文件
def openfile():
    sfname = filedialog.askopenfilename(title='选择文件', filetypes=[('All Files', '*')])
    return sfname


#打开文件并处理
def openshow():
    global  root
    text1.delete('1.0', 'end')
    printToGUI("begin to process file")
    filename=openfile()
    printToGUI("please open file")

    zipfile = rename_file_to_zip(filename)
    if  zipfile != 0 :
        files_dir = un_zip(zipfile)
        rename_file_to_xps(zipfile)

        printToGUI("unzip file %s end" % filename)
        processData(files_dir)
    else:
        printToGUI(" %s is not a correct file"%filename)

    clearFolders(files_dir)




def processData(folders):

    list_signals = getSignals()
    map_data ={}
    folder_name = r'%s\Documents\1\Pages' % folders
    printToGUI("begin to process files saved in {}:".format(folder_name))
    file_names = getFileNames(folder_name)
    printToGUI("files need to process :" + str(file_names))
    #获取文件中的药物名称
    list_medicine = get_medicine_name_from_file()
    printToGUI("Please check:medicine list-- " + str(list_medicine))

    for i in range(len(file_names)):
        printToGUI("begin to process " + file_names[i])
        map_data[i] = processSinglePage(list_medicine, list_signals, file_names[i])

    writedata(map_data,folders)
    printToGUI("save data to file:%s.xls finished"%folders)


#重命名文件，修改文件后缀为压缩文件，方便后续处理
def rename_file_to_zip(filename, suffix = '.zip') -> object:
    portion = os.path.splitext(filename)
    file_suffix = str(portion[1]).lower()
    if file_suffix == ".xps":
        newname = portion[0] + suffix
        filename = filename
        os.rename(filename, newname)
        return newname
    else:
        printToGUI("please input the correct file end with .xps")
        return 0

#重命名文件，修改文件后缀为xps,还原文件
def rename_file_to_xps(filename, suffix = '.xps') -> object:
    portion = os.path.splitext(filename)
    file_suffix = str(portion[1]).lower()
    if file_suffix == ".zip":
        newname = portion[0] + suffix
        filename = filename
        os.rename(filename, newname)
        return newname
    else:
        printToGUI("please input the correct file end with .zip")
        return 0


def clearFolders(filePath):
    shutil.rmtree(filePath)

def un_zip(file_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    portion = os.path.splitext(file_name)
    uncompress_dir = portion[0]
    if os.path.isdir(uncompress_dir):
        print(uncompress_dir + " is existed")
        pass
    else:
        os.mkdir(uncompress_dir)
        print(uncompress_dir + " is not existed,created")
    for names in zip_file.namelist():
        print("unzip " + names)
        zip_file.extract(names,uncompress_dir+ "/")
    zip_file.close()
    return uncompress_dir




def printToGUI(strlog):
    text1.insert('end', strlog)
    text1.insert(tk.INSERT, '\n')
    text1.see(tk.END)
    text1.update()

global root
root = tk.Tk()
root.title("打开文件")
root.geometry("800x600")
B1 = tk.Button(root, text="打开文件", command=openshow)
B1.place(x=20,y = 5,width=70, height=35)


text1= tk.Text(root,bd =5)
text1.place(x=20,y=45,width=700, height=400)
text1.see(tk.END)

label1 = tk.Label(root, text="本程序仅供测试使用，不对数据准确性负责，请仔细核对，谨慎使用！",foreground = 'red')
label1.place(x=20,y = 500,width=700, height=20)

root.mainloop()
