# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 14:19:49 2017
ログデータを５秒間毎に区切るプログラム（ハプティクス用）

@author: student
"""

import pandas as pd
import os
import csv
import shutil

#dir_name = ['haptics']
#dir_name = ['haptics_finger']
#dir_name = ['haptics2']
dir_name = ['haptics3']

dir_i = 0
dir_path = r'/Users/student/Documents/data/'+dir_name[dir_i]+r'/'
out_dir_path = r'/Users/student/Documents/data/'+dir_name[dir_i]+r'_csv/'

if os.path.isdir(out_dir_path) is False:
    os.makedirs(out_dir_path)
    print("make dir")
else:
    shutil.rmtree(out_dir_path)
    print("delete dir")
    os.makedirs(out_dir_path)
    print("make dir")


data = []
files = os.listdir(dir_path)
count = 0
for file in files:
    data = []
    print (file)
    f = open(dir_path+file, 'rb')
    for line in f:
#        print(line)
        data.append(line)

    
        if len(data) > 166: # 167*30 = 5010ms every 5sec save
            print(len(data))
            df = pd.DataFrame(data)
            save_data = open(out_dir_path+file.split('.')[0]+str(count)+'.csv','w')
#            writer = csv.writer(save_data)
#            writer.writerow(data)
            df.to_csv(save_data,header=None, index=None)
            save_data.close()
            data = []
            count += 1
    f.close()