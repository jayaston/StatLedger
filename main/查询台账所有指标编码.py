# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 15:51:55 2019

@author: XieJie
"""
import sys
sys.path.append(r'E:\pyworks\StatLedger\module')
import shujuyuan as sj

result = sj.Datataizhang().get_all_quota()
result.to_excel('所有在用指标.xlsx')