# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 18:45:49 2017
線形補間　完全バージョン
（非数値(--100,"","-",.etc)、\x00削除、ファイル長さ不足、ディレクトリファイル全てに対応し、線形補間後の値を保存できる）
補間後だけでなく、補間前も保存可能
@author: student
"""

import re
import os
import pandas as pd
import shutil
#import numpy as np


#dir_name = ['open_12_18_csv','clatter_12_18_csv']
#dir_name = ['ballpen','pencil']
#dir_name = ['sku186-580','sku445-753','sku469-657']
dir_name = ['ballpen','marker','sharppen']

#dir_i = 0
#dir_i = 1
dir_i = 2

#dir_path = r'/Users/student/Documents/data/haptics_finger_csv/'+dir_name[dir_i]+'/'
#out_dir_path = r'/Users/student/Documents/data/haptics_finger_csv/'+dir_name[dir_i]+'_beforelinear/'
#out_dir_path = r'/Users/student/Documents/data/haptics3_csv/'+dir_name[dir_i]+'_beforelinear/'

#dir_path = r'/Users/student/Documents/data/'+dir_name[dir_i]+'/'
dir_path = r'/Users/student/Documents/data/haptics3_csv/'+dir_name[dir_i]+'/'
#out_dir_path = r'/Users/student/Documents/data/'+dir_name[dir_i]+'_beforelinear/'
out_dir_path = r'/Users/student/Documents/data/haptics3_csv/'+dir_name[dir_i]+'_afterlinear/'


files = os.listdir(dir_path) # get all files
#file = files[1]
#print("file:{}".format(file))


if os.path.isdir(out_dir_path) is False:
    os.makedirs(out_dir_path)
    print("make dir")
else:
    shutil.rmtree(out_dir_path)
    print("delete dir")
    os.makedirs(out_dir_path)
    print("make dir")
   

# 非数値がある場合、その値の代わりとして1111をtmp_acc_listに追加し、
# tmp_acc_listの削除する列のindexを決めるアルゴリズム
# 1111を追加する理由は、数値のみが追加されていくプログラムとなっており、
# 非数値は何かしらの値（ここでは1111）を入力しておかなければ、もとのsignalの個数と一致しなくなるため

def decideDelete(index,delete_idx,signal): 
    tmp_acc_list[index%3].append(1111) # 破損個所を明確化するために、絶対ありえない数字を
    
    if index%3 == 0:
        delete_idx += (index,index+1,index+2)
    elif index%3 == 1:
        delete_idx += (index-1,index,index+1)
    else:
        delete_idx += (index-2,index-1,index)
    print("signal:{}------>del_index:{}".format(signal,delete_idx))
    return(delete_idx)

# delete_idxの値を削除するアルゴリズム
def deleteProcessing(delete_idx,tmp_acc_list,tmp_timestamps):
    print("before_acc_list:{}".format(tmp_acc_list))                
    
    for i in delete_idx:
        print("i:{}".format(i))
        del_idx = tmp_acc_list[i%3].pop(int(i/3))
        print("acc_list_del:{}".format(del_idx))
        
        if i%3 == 0:
            print("tmp_times:{}".format(tmp_timestamps))
            tmp_timestamps.pop(int(i/3))
            print("tmp_times:{}".format(tmp_timestamps))
        
    print("after_acc_list:{}".format(tmp_acc_list))
    
       
RANGE = 10

# 線形補間  
def linear(arg,axis):
    time = []
    y = []
    # 線形補間 
    for j in range(0,int(len(acc_list[arg])/10)):     
    #    if j > 2:
    #        break
        for i in range(0,RANGE):
    #        print(i+(j*(RANGE)))   
    #        print(i+(j*(RANGE-1)),i+1 + (j*(RANGE-1)))
    
            # 2値の差（0~３msなら、3ms間の差があり、0ms, 1ms, 2ms）の線形補間の値をyに格納する
            # なので、3msの値が格納されなくなる
            # そのため、3msのときのyを格納する処理
            if j ==  int(len(acc_list[arg])/10)-1 and i == RANGE-1:
    #            print(":{}".format(i+1 + (j*(RANGE-1))))
    #            tmp = x[i+1+(j*(RANGE-1))] 
    #            print("tmp:{}".format(round(tmp,2)))
    #            print(acc_list[0][i+1+(j*(RANGE-1))])
                y.append(acc_list[arg][i+(j*RANGE)])
                break
            
            # 2 degree equation
            # y1 = ax1 + b
            # y2 = ax2 + b
            # a,bを求め
            # y = ax + b
            y1 = acc_list[arg][i +(j*RANGE)]
            y2 = acc_list[arg][i+1 + (j*RANGE)]
            x1 = timestamps[i+(j*(RANGE))]
            x2 = timestamps[i+1 + (j*(RANGE))]
                        
            a = (y1-y2) / (x1-x2)
            b = ((y2*x1) - (y1*x2)) / (x1-x2)
#            ans = a*x1 + b
    #        print(j,x1,y1,x2,y2,a,b,ans)       
    #        print("num:{}".format(i+(j*RANGE)))
    #        print("{}-{}={}".format(i+1 + (j*(RANGE-1)),i +(j*(RANGE-1)),round(timestamps[i+1 + (j*(RANGE-1))] - timestamps[i +(j*(RANGE-1))],2)))     
            print("{}-{}={}".format(i+1 + (j*(RANGE-1)),i +(j*(RANGE-1)),timestamps[i+1 + (j*(RANGE-1))] - timestamps[i +(j*(RANGE-1))]))     
    
            tmp = timestamps[i+(j*(RANGE))] 
    #        print("tmp:{}".format(tmp))
            
                
            # 2値の差（0~３msなら、3ms間の差があり、0ms, 1ms, 2ms）の線形補間の値をyに格納する
            for k in range(0,timestamps[i+1 + (j*RANGE)] - timestamps[i +(j*RANGE)]):
    #            print(tmp,round(a*tmp + b))
                y.append(round(a * tmp + b))
    #                print("3:{}".format(round(tmp,2)))
                tmp += 1
    
    
    data = []     
    time = []
    # dataに一定間隔（3ms）でy値を取り出す
    # timeに3msでtimestampsを格納する
    for i in range(0,len(y),3):
        data.append(y[i])
        time.append(timestamps[0]+i)
        
    #print(len(data))
    #print(len(time))
    
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    mpl.rc('figure.subplot',left=0,hspace=0.5,wspace=0,bottom=0,top=1.0)
    
    plt.clf()
    plt.subplot(211)
    plt.plot(timestamps,acc_list[arg],label="before",marker="o")
    plt.legend()
    plt.title("{}".format(axis))
    plt.xlabel("Time[ms]")
    plt.ylabel("accelerometor[m/s^2]")
    
    plt.subplot(212)
    plt.plot(time,data,label="after",marker="o")
    plt.title("{}".format(axis))
    plt.legend()
    plt.xlabel("Time[ms]")
    plt.ylabel("accelerometor[m/s^2]")
    
    return (time,data)
    

pattern = [r"^-?[0-9]{1,3}"]
r = re.compile(pattern[0])

for file in files:
    print("file:{}".format(file))    
    f = open(dir_path+file, 'rb')
    

    acc_list = [[], [], []] # acc_list[[x],[y],[z]] all data
    timestamps = [] # timestamps[time[ms]] all data 

    for line in f:
        tmp_acc_list = [[],[],[]] # tmp_acc_list = [[x],[y],[z]] 1 row data
        tmp_timestamps = []  # tmp_timestamps[time[ms]] 1 row data
        delete_idx = ()    # delete_idx(index)
        signal = str(line).replace(r'\x00', "").split(',') #signal= [id,timestamps,status,x,y,z,...,x,y,z] length=33 
        print(len(signal))
        
        if signal[0] == 'b\'"b\\\'[810f0413' and len(signal) > 2: # ID check   
    #        print(len(signal))
    #        print(signal)

#            if len(signal[1]) < 5: # value
#                timestamp = int(signal[1])
#            else:
#                print("yeah")
#                continue

            pattern1 = [r"[a-z]"]
            r1 = re.compile(pattern1[0])
            match1 = r1.search(signal[1])
            
            if match1 is None: 
                timestamp = int(signal[1])
            else:
                continue
            
            signal = signal[3:] 
                   
#            print(signal)
            if len(timestamps) > 0 and abs(timestamps[-1] - timestamp) > 1000: # timestampsの差が大きいなら初期化(1000ms = 1s)
#                    print(timestamps[-1],timestamp,abs(timestamps[-1] - timestamp))
                timestamps = []
                acc_list = [[],[],[]]                    
#                print(match.group())
            if len(signal)%3 != 0:
                print("before_signal_pop:{}".format(signal))
                for d in range(len(signal)%3):
                    sig_pop = signal.pop()
                print("after_signal_pop:{}".format(signal))
                  
            
            for i in range(len(signal)): # all value check            
                if i%3 == 0: # timestamps
                    tmp_timestamps.append(timestamp)
                    timestamp += 3

                match = r.search(signal[i])
                if not match is None: # value
#                            print("match:{}".format(match.group()))
                    tmp_acc_list[i%3].append(int(match.group()))                     
                else: # not value (decide the delete index)
                    delete_idx = decideDelete(i,delete_idx,signal)
                
            if len(delete_idx) != 0: # is delete_idx
                del_idx = list(delete_idx)
                del_idx.sort(reverse=True)
                deleteProcessing(del_idx,tmp_acc_list,tmp_timestamps)            

                
            for i in range(3):
                acc_list[i%3].extend(tmp_acc_list[i])
            timestamps.extend(tmp_timestamps)

                            
    print("x:{}".format(len(acc_list[0])))
    print("y:{}".format(len(acc_list[1])))
    print("z:{}".format(len(acc_list[2])))
    
    x_data = []
    y_data = []
    z_data = []
    t = []
    datas = [[],[],[]]
    
    t,x_data = linear(0,"x")
    t,y_data = linear(1,"y")
    t,z_data = linear(2,"z")
    
    
    datas[0].append(x_data)
    datas[1].append(y_data)
    datas[2].append(z_data)
    
    
#    # 補間前を保存
#    if len(x_data) > 800:  
#        out_f = open(out_dir_path+file, 'w')         
#        df = pd.DataFrame({"x":acc_list[0],
#                           "y":acc_list[1],
#                           "z":acc_list[2]}).T
#        
#        df.to_csv(out_f,header=None,index=None)
#        out_f.close()
    
    # 補間後を保存
    if len(x_data) > 800:  
        out_f = open(out_dir_path+file, 'w')         
        df = pd.DataFrame({"x":x_data,
                           "y":y_data,
                           "z":z_data}).T
        
        df.to_csv(out_f,header=None,index=None)
        out_f.close() 
                     

        
    f.close()
    
 


    
    
