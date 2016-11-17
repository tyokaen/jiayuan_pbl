# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 22:44:59 2016

@author: student
"""


import os
import re
import pandas as pd
import numpy as np
            
            
def find_files(director):
    for root, dirs, files in os.walk(director):
#        print ("root:%s" % root)
#        print ("dirs:%s" % dirs)
        print ("files:%s" % files)
        yield root
        for file in files:
         yield os.path.join(root, file)
count=0
for file in find_files('C:/Users/student/.spyder-py3/result/'):
    target = r"\.csv"
    # targetと一致した文字列の最初の１つを返す
    match_string = re.search(target, file)
    if match_string:
        #print(match_string.group())
        #print(file)
        print("count:%s" % count)
        df = pd.read_csv(file,header=None,error_bad_lines=False)
        df_d = df.dropna()
        df_t = df_d.T

        if len(df) < 10:
            count += 1
            continue
        
        
        df_union = list(df_t[0])
        
        # 要らない情報を削除(前)
        trush_1 = df_union.pop(0)
        trush_2 = df_union.pop(0)
        trush_3 = df_union.pop(0)
        
        # 要らない情報を削除(後)
        trush_4 = df_union.pop() 
        target = r"]"
        p = re.search(target, trush_4)
#        print(p)
#        print(len(df_union))
#        print(p.start())
#        
        
        # ]の文字だけ取り除き、一番最後に追加
        add_string = trush_4[0:p.start()]
        df_union.append(add_string)
        df_union = np.array(df_union).astype(float)
        
        for row in df_t:
#            print("row:%s" % df_t[row])
            df_array = list(df_t[row])
        
            # 要らない情報を削除(前)
            trush_1 = df_array.pop(0)
            trush_2 = df_array.pop(0)
            trush_3 = df_array.pop(0)
            
            # 要らない情報を削除(後)
            trush_4 = df_array.pop() 
            target = r"]"
            p = re.search(target, trush_4)
            if p is None:
                count += 1
                continue
#            print(p)
#            print(len(df_array))
#            print(p.start())
            
            # ]の文字だけ取り除き、一番最後に追加
            add_string = trush_4[0:p.start()]
            df_array.append(add_string)
            df_array = np.array(df_array).astype(float)
            df_union = np.vstack([df_union, df_array])
            
            
        # 余分な行を削除
        df_union = df_union[1:]
################################################################################
#　　　　　　　　　　　　　　　　　　　　　　csvファイルに書き込む
################################################################################

        count += 1