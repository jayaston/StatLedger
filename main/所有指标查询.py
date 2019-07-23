# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 15:51:55 2019

@author: XieJie
"""

import pandas as pd
import cx_Oracle


conn = cx_Oracle.connect("zls_tjfx/tjfx10goracle@10.1.12.196:1521/orcl") 
sql2 = "SELECT * \
            FROM zls_tjfx.cs_Quota_Define"
df_zhibiao = pd.read_sql(sql2,conn)
df_zhibiao.info()
df_zhibiao.query("EFFECTYPE == 'Y'",inplace = True)

result = df_zhibiao[['QUOTA_CODE','QUOTA_NAME','REMARK','QUOTA_FULL_NAME']].drop_duplicates(['QUOTA_CODE','QUOTA_NAME'])
result.to_excel('所有在用指标.xlsx')