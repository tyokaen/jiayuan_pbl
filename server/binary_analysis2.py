# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 16:09:57 2017
バイナリデータを10進数に変換する
acc : 変換前16進数
lines : 変換後10進数（全て）
@author: student
"""


import os
from struct import unpack
import re
import binascii
import numpy as np

dir_name = ['binary']
dir_i = 0
dir_path = r'/Users/student/Documents/data/'+dir_name[dir_i]+'/'
out_dir_path = r'/Users/student/Documents/data/'+dir_name[dir_i]+'_linear/'


files = os.listdir(dir_path) # get all files
files = files[2:]


for file in files:
    print("file:{}".format(file))    
#    f = open(dir_path+file, 'rb')

file = files[0]
f = open(dir_path+file, 'rb')

#tmp = f.read(4).encode("hex") # fail
#print(repr(f.read()))

bin_tostr = repr(binascii.b2a_hex(f.read()))
bin_data = bin_tostr[2:-1]



micon_id = []
mode = []
timestamp = []
acc_list = [] # acceleration
line = []
lines = []
acc_lists = []
dust_box_16 = []
dust_box_10 = []


for idx,binary in enumerate(bin_data):
#    print("idx:{}".format(idx))
#    if idx > 138:
#        break

#    print("bin_data:{}".format(bin_data[idx:idx+8]))
    if bin_data[idx:idx+8] == '8102178b':

        # micon_id抽出・変換
        micon_id.append(bin_data[idx:idx+8] )

        # mode抽出・変換
        mode.append(binascii.a2b_hex(bin_data[idx+8:idx+10]))
        
        # timestamp抽出
        timestamp.append(bin_data[idx+10:idx+16])
        
        # acc_list抽出
        acc_list.append(bin_data[idx+16:idx+136])

        print("id:{}/mode:{}/timestamp:{}/acc_list:{}".format(micon_id,mode,timestamp,acc_list))
        print("id:{}/mode:{}/timestamp:{}/acc_list:{}".format(len(micon_id[0]),len(mode[0]),
                                                              len(timestamp[0]),len(acc_list[0])))

        # タイムスタンプ10進数変換
        new_timestamp = []
        for d in timestamp:
#            print("btimestamp:{}".format(d))
            target = re.compile(r'ff')
            match = target.findall(d)
            if len(match) == 0:
                new_timestamp.append(int(d,16))
            else:
                new_timestamp.append(int(d.replace('ff','00'),16))
#            print("new_timestamp:{}".format(new_timestamp))
        timestamp = []
        timestamp.extend(new_timestamp)
        print("timestamp:{}".format(timestamp))

        
        # acc_list10進数変換
#        print("bacc_list:{}".format(acc_list)) # 変換前
        acc = []
        for d in range(int(len(acc_list[0])/4)):
#            print("index".format(d))
#            print("acc_list[0]:{}".format(acc_list[0][d*4:d*4+4]))

            if acc_list[0][d*4:d*4+4] =='06a4': #1700
#                print("06a4:{}".format('00'+acc_list[0][d*4+2:d*4+4]))
                acc.append('0000')
            elif acc_list[0][d*4:d*4+2] == '07':
#                print("07:{}".format('00'+acc_list[0][d*4+2:d*4+4]))
                acc.append('00'+acc_list[0][d*4+2:d*4+4])
            else:
#                print("nofix:{}".format(acc_list[0][d*4:d*4+4]))
                acc.append(acc_list[0][d*4:d*4+4])                
            
#            elif d % 2 == 0: #偶数
#                print("acc_list:{}".format(acc_list[0][d*4:d*2+2]))
#                if acc_list[0][d*4:d*4+2] == '07':
#                    print("07:{}".format('00'+acc_list[0][d*4+2:d*4+4]))
#                    acc.append('00'+acc_list[0][d*4+2:d*4+4])
#                else:
#                    acc.append(acc_list[0][d*4:d*4+4])
#            else: # 奇数
#                acc.append(acc_list[0][d*4:d*4+4])


        acc_lists.append(acc)
        
#        print()
#        print("acc:{}".format(acc,end="")) # 変換後
        new_acc = []
        for d in acc:
            new_acc.append(int(d,16))

        
        new_acc_list=[] # signed 10進数変換
        for d in new_acc:
            if d >= 65280 and d < 65535: # 65280(-256) < d < 65535(-1)16 
                signed = d - 65536
                new_acc_list.append(signed)
                print("-256<signed:{}<-1".format(signed))
            elif d >127 and d <= 256:
                signed = d - 256
                new_acc_list.append(signed)
            else:
                new_acc_list.append(d)
#        print()
#        print("new_acc_list:{}".format(new_acc_list,end=""))
                
        delete = []
        delete_index = []
        for idx,d in enumerate(new_acc_list):
            if d > 255:
                dust_box_16.append(hex(d))
                dust_box_10.append(d)
                print("ddddd:{}".format(d))
                print(int(idx-idx%3),int((idx-idx%3)+1),int((idx-idx%3)+2))
                delete.append(int(idx-idx%3))
                delete.append(int(idx-idx%3)+1)
                delete.append(int(idx-idx%3)+2)
                delete_idx = set(delete)
                delete_index = list(delete_idx)
                delete_index.sort(reverse=True)
#                new_acc.append(int(d,16))
#            else:
#                new_acc.append(int(d,16))
#        print("new_acc:{}".format(new_acc,end=""))
 
#        delete_index = list(delete_idx)
#        delete_index.sort(reverse=True)
        
        if len(delete_index) > 0:
            print("delete_sort:{}".format(delete_index))
            print("new_acc_list:{}".format(new_acc_list,end=""))
            for de in delete_index:
                print("new_acc_list:{}/de:{}".format(new_acc_list[de],de))
                new_acc_list.pop(de)

            print("dnew_acc:{}".format(new_acc_list),end="")
            delete_idx = {}
            print("dx:{}".format(delete_idx))

            
#        print("new_acc:{}".format(new_acc,end=""))

 
        line.extend(micon_id)
        line.extend(mode)
        line.extend(timestamp)
        line.extend(new_acc_list)           
        lines.append(line)
        
        micon_id = []
        mode = []
        timestamp = []
        acc_list = [] # acceleration
        line = []
    

f.close()








