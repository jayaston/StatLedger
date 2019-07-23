# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 08:31:59 2019

@author: XieJie
"""
#
import sys
sys.path.append(r'E:\pyworks\StatLedger\module')
import pandas as pd
import numpy as np
import shujuyuan as sj
#import re    



list1 = [
         ['1001','00752','m'],
         ['1002','00752','m'],
         ['1003','00752','m'],
         ['1004','00752','m'],
         ['1005','00752','m'],
         ['1007','00752','m']
         ]
shuju_df = sj.Datataizhang().getdata('20140101','20181231',list1)

shuju_df.info()

shuju_df.QUOTA_VALUE = pd.to_numeric(shuju_df.QUOTA_VALUE,errors='coercs').fillna(0)

test = pd.pivot_table(shuju_df,index = ['QUOTA_DATE','QUOTA_NAME'],columns = 'GROUP_NAME',values='QUOTA_VALUE')
print(test)
test.to_excel(r'E:\pyworks\数据查询.xlsx')