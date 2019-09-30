# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 08:39:30 2019

@author: XieJie
"""
#sys.path.append(r'E:\pyworks\StatLedger\module')
#import sys
import pandas as pd
#import numpy as np
from tjfxdata import TjfxData
import re   
#import cx_Oracle
def order_gongshiku():
        gongshiku = pd.read_excel(r'../数据表/日数据汇总公式库.xlsx','layer3',dtype='object')
    
        gongshiku = gongshiku.drop(['zbming'],axis=1)
        
        gongshiku['zhibiao'] = gongshiku['RECORD_TYPE']+'_'+gongshiku['var_dept']+'_'+gongshiku['var_code']
            
        
        def newformula(x):#对通用公式进行还原函数
            result = re.sub(r'(?=\b_)', x['var_dept'],x['setformula'])
            result = re.sub(r'(?<=_\b)', x['var_code'],result)
            result = re.sub(r'(?=\b\d+_)', x['RECORD_TYPE']+'_',result)
            return result
        
        gongshiku['setformula'] = gongshiku.apply(newformula,axis=1)
        gongshiku['zhibiaoji'] = gongshiku.apply(lambda x: re.findall(r'\b[a-z]_\d+_\d+\b',x['setformula']),axis=1)
        gongshiku.drop(['var_code','var_dept'],axis=1,inplace=True)      

        return gongshiku

def get_castdata(startd,endd,quota):    
    quotalist=quota.split('_')    
    quotalist.append(quotalist.pop(0))
    quotalistall = []
    quotalistall.append(quotalist)
    result = TjfxData().getdata(startd,endd,quotalistall)
    result.QUOTA_VALUE = pd.to_numeric(result.QUOTA_VALUE,errors='coercs').fillna(0)
    result_dcast = pd.pivot_table(result,index='QUOTA_DATE',
                                columns=['RECORD_TYPE','QUOTA_DEPT_CODE','QUOTA_CODE'],
                                values = 'QUOTA_VALUE' )  
    new_colnames = ["_".join(list(i)) for i in list(result_dcast.columns)]    
    result_dcast.columns=new_colnames
    return result_dcast

def calculate_quota(startd,endd,quota):
    
    formula = gongshiku[gongshiku.zhibiao == quota].iat[0,1]
    zhibiaoji = gongshiku[gongshiku.zhibiao == quota].iat[0,3]
    for i in zhibiaoji:
        exec(i + "= cum_quota (startd,endd,i)") 
#        locals()['name'] = 3
    result = eval(formula)
    return result


def cum_quota (startd,endd,quota):
    gongshiku = order_gongshiku()
    if quota in list(gongshiku.zhibiao):
        result = calculate_quota(startd,endd,quota)
    else:        
        result = sum(get_castdata(startd,endd,quota).to_dict('list').get(quota,[0]))
    return result

if __name__ == "__main__" :    
       
    startd,endd,quota = '20190901','20190926','d_00_01464'
    test = cum_quota(startd,endd,quota)


  
 
