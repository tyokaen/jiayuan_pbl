# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 09:51:32 2017
振動データ一定サイズ(WAVE_NUM)のウェーブレットデータ変換するプログラム
@author: student
"""

import pywt
import csv
import os
import re
import shutil

target = r'^-?[0-9]{1,3}'
r = re.compile(target)

dir_name = ['02-01＿door-open_csv_afterlinear','02-01_clatter_csv_afterlinear']

dir_i = 0
#dir_i = 1
dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'\\'
out_dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'_wavelet\\'
files = os.listdir(dir_path)


if os.path.exists(out_dir_path) is False:
    os.makedirs(out_dir_path)
    print("make dir")
else:
    shutil.rmtree(out_dir_path)
    print("delete dir")
    os.makedirs(out_dir_path)
    print("make dir")
    


for file in files:
    f = open(dir_path + file, 'r')
    w = open(out_dir_path+file, 'a')
    
    csvWriter = csv.writer(w)
    data = list(f)
    data_list = []
    acc_list = [[],[],[]]

    for d in data:
#        print(d.split(","))
        data_list.append(d.split(","))
    
    for i,d in enumerate(data_list):
#        print("index:{}".format(i))
        for value in d:
#            print("value:{}".format(value))
            match = r.search(value)
            if match is None:
                print("oh my god")
            else:
#                print(match.group())
                acc_list[i].append(match.group())
            
    WAVE_NUM = 10 #特徴量数を決める
    for i in range(0,3):
        coeffs = pywt.wavedec(acc_list[i], 'db1', level=7)
#        print("coeffs_len:{}".format(len(coeffs[0])))
        if len(coeffs[0]) >= WAVE_NUM:
            csvWriter.writerow(coeffs[0][0:WAVE_NUM])
        else:
            if os.path.exists(out_dir_path+file):
                w.close()
                os.remove(out_dir_path+file)
                break

    f.close()
    w.close()


