# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 15:35:26 2019

@author: XieJie
"""
import sys
sys.path.append(r'E:\pyworks\StatLedger\module')
import xlrd
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import pandas as pd
import numpy as np

def open_excel(path):
    try:
        book = xlrd.open_workbook(path)  #文件名，把文件与py文件放在同一目录下
    except:
        print("open excel file:"+path+"failed!")
    try:
        sheet = book.sheet_by_index(0)   #execl里面的worksheet1
        return sheet
    except:
        print("locate worksheet0 in excel file:"+path+"failed!")


def load_datacode():
    data_code = pd.read_excel(r'E:\pyworks\行业报表指标与台账指标编码对应表.xlsx',sheet_name=2,dtype={'台账编码':np.object,'对应报表中指标名称':np.object})
    
    return data_code
   
#    set(data_code[ data_code.duplicated('对应报表中指标名称')]['对应报表中指标名称'])
def load_deptcode():
    dept_code = pd.read_excel(r'E:\pyworks\行业部门与台账部门编码对应表.xlsx',sheet_name=0,dtype={'部门':np.object,'编码':np.object})
    
    return dept_code   
    
def load_data(path):
    dept_code = load_deptcode()
    data_code = load_datacode()
    sheet = open_excel(path)    
    hangye_rows = sheet.col_values(0).index('大用户:(当月用5万立方米以上用户)')-6
    hangyelist = []
    thedatetime = xlrd.xldate_as_datetime(sheet.cell(4,6).value, 0)
    quota_date = thedatetime.strftime('%Y-%m-%d %H:%M:%S')
    mon = thedatetime.strftime('%Y%m')
    quota_dept = sheet.cell(4,1).value
    quota_dept_code =str( list(dept_code[dept_code['部门']==quota_dept]['编码'])[0] )   
    record_type = 'm'
    for j in range(2,sheet.ncols-1):
        for i in range(7, hangye_rows):
            quota_value = str(sheet.cell(i,j).value)
            if quota_value != '' : 
                quota_name = sheet.cell(5,j-1 if j%2==1 else j).value+sheet.cell(i,0).value+sheet.cell(6,j).value
                if quota_name in list(data_code['对应报表中指标名称']):
                    quota_code = str(list(data_code[data_code['对应报表中指标名称'] == quota_name]['台账编码'])[0] ) 
                    value = (quota_code,mon,quota_date,quota_value,'',quota_dept_code,'','',record_type)
                    hangyelist.append(value)
                    
    return hangyelist


def dir_data(dirpath):
    allfiles = []            
    for root,dirs,files in os.walk(dirpath): 
        for file in files:
            allfiles.append(os.path.join(root,file))   
    alldata=list(map(load_data,allfiles))
    totallist =[]
    for i in alldata:    
        for j in i:
            totallist.append(j)
    totallist = list(set(totallist))
    return totallist 
  




if __name__ == "__main__" :    
    test = dir_data(r'E:\pyworks\行业表')
    import shujuyuan as sj    
    sj.Datataizhang().importdata(test)
    
    
#df = pd.read_excel('HSR_RPT_SALE_NET.xls',header=None)

