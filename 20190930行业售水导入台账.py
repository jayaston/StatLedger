# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 15:35:26 2019

@author: XieJie
"""
import sys
sys.path.append(r'E:\pyworks\StatLedger\module')
from hangyebiaototjfx import dir_data
import tjfxdata as tjfx

test = dir_data(r'E:\pyworks\行业表')
tjfx.TjfxData().importdata(test)
    
    
#df = pd.read_excel('HSR_RPT_SALE_NET.xls',header=None)

