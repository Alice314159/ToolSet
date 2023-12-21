# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import xlwt
import os
import re
import sys
import importlib
importlib.reload(sys)
#sys.setdefaultencoding('utf8')

Isolate = "Isolate"
IsolateEng = "isolate"
IsolateChg = "菌株"
def get_medicine_name_from_file(fileName ='medicineName.ini' ):
    list_medicine = [IsolateEng]

    with open(fileName, "r",encoding='utf-8') as myfile:
        for line in myfile:
            list_medicine.append(line.lower().strip())

    return list(set(list_medicine))

def get_medicine_name(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    xx = root.getchildren()
    list_name = []
    pattern = re.compile(r'([a-z]+)*(\d+(\.\d{1-4}})?)', re.I)  # re.I 表示忽略大小写

    for child in xx:
        datas = child.attrib
        if "UnicodeString" in datas.keys():
            content = datas["UnicodeString"]
            if pattern.search(content):
                print('temp medicine name ', content)
                if content.endswith('NI'):
                    list_name.append(content)
                if content.endswith('S'):
                    list_name.append(content)
                if content.endswith('IE'):
                    list_name.append(content)

    #将nameList进行处理
    medicine_list = [IsolateEng,IsolateChg]
    pattern = re.compile(r'([a-z]+)', re.I)  # re.I 表示忽略大小写
    for name in list_name:
        m = pattern.match(name)
        print(m.group(0))
        medicine_list.append(m.group(0))

    return medicine_list

def getSignals():
    list_data = []
    list_data.append(">=")
    list_data.append("<=")
    list_data.append("=")
    list_data.append(">")
    list_data.append("<")
    return list_data

def getValidData(medicineName,indata,list_signals):
     strdata = indata.replace("\"","")
     isFindSignal = False
     for i in range(len(list_signals)):
        if strdata.find(list_signals[i])>0:
            isFindSignal = True
            signal = list_signals[i]
            list_data = strdata.split(signal)
            key = medicineName
            value = signal + list_data[1]
            return (medicineName,value)

     if isFindSignal == False:
         list_data = strdata.split(medicineName)
         return (medicineName,list_data[1])


def processSinglePage(list_medicine, list_signals, filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    map_page = {}
    isFindIsolate = False
    xx = list(root)
    dataSecitonName = "UnicodeString"
    for child in xx:
        datas = child.attrib
        if dataSecitonName in datas.keys():
            content = datas[dataSecitonName].lower()
            if isFindIsolate == True:
                map_page[IsolateEng] = content
                isFindIsolate = False

            if content.find(IsolateEng) > -1 or content.find(IsolateChg) > -1:
                isFindIsolate = True

            for i in range(len(list_medicine)):
                dataList = content.split(list_medicine[i])
                if len(dataList) > 1 and content.startswith(list_medicine[i]):
                    map_page[list_medicine[i]] = dataList[1]
                    print(content, list_medicine[i],dataList[1])
                    break

    return map_page


def writedata(map_data,xls_name):
    f = xlwt.Workbook(encoding='utf-8')
    sheet1 = f.add_sheet('data')
    # 写第一行，药名
    final_medicine_list = list(map_data[0].keys())
    print(final_medicine_list)
    for i in range(0, len(final_medicine_list)):
        sheet1.write(0, i+1, final_medicine_list[i].capitalize())

    nPage =0
    for page,value in map_data.items():
        nPage = nPage +1
        for j in range(len(final_medicine_list)):
            if final_medicine_list[j]  in value.keys():
                sheet1.write(nPage, j+1, value[final_medicine_list[j]])
                print('write nPage{} data --{}：{}'.format(nPage,str(final_medicine_list[j]),str(value[final_medicine_list[j]])))
            else:
                print('nPage{} has not find medicine name:{} '.format(nPage,str(final_medicine_list[j])))

    f.save('%s.xls'%xls_name)

def getFileNames(path):
    L = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.fpage'):
                L.append(os.path.join(root, file))
    return L



if __name__ == '__main__':
    get_medicine_name_from_file()
    list_signals = getSignals()

    map_data ={}
    file_names = getFileNames(r'E:\CODE\DealXPS\2019RRTB0317\\Documents\\1\\Pages')
    list_medicine = get_medicine_name(file_names[0])

    for i in range(len(file_names)):

        map_data[i] = processSinglePage(list_medicine, list_signals, file_names[i])

    writedata(list_medicine,map_data,"2018HUNAN20210414")












