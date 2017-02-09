# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 16:45:29 2017
線形補間した値を読み込み、fft
@author: student
"""


import os
import pandas as pd
import numpy as np
from scipy import  hamming
from scipy.fftpack import fft,fftfreq
import matplotlib.pyplot as plt


#--------------------------------------------------------------------------------------------#
                                    # 振動データの保存先を指定--start
#--------------------------------------------------------------------------------------------#
#dir_name = ['open_12_18_csv_linear','clatter_12_18_csv_linear']
#dir_name = ['open_12_18_csv_beforelinear','clatter_12_18_csv_beforelinear']
#dir_name = ['open_12_18_csv_afterlinear','clatter_12_18_csv_afterlinear']
#dir_name = ['ballpen_afterlinear','pencil_afterlinear']
#dir_name = ['ballpen_beforelinear','pencil_beforelinear']
#dir_name = ['sku445-753_finger_afterlinear','sku469-657_finger_afterlinear']
#dir_name = ['sku186-580_afterlinear','sku445-753_afterlinear','sku469-657_afterlinear']
#dir_name = ['sku186-580_beforelinear','sku445-753_beforelinear','sku469-657_beforelinear']
#dir_name = ['ballpen_afterlinear','marker_afterlinear','sharppen_afterlinear']
dir_name = ['pen_csv_afterlinear2','tile_csv_afterlinear2']
#dir_name = ['02-01＿door-open','02-01_clatter']


dir_i = 0
#dir_i = 1
#dir_i = 2
#file_i = dir_i

dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'\\'
#--------------------------------------------------------------------------------------------#
                                    # 振動データの保存先を指定--end
#--------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------#
                                    # 振動データの出力先を指定--start
#--------------------------------------------------------------------------------------------#
#dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'\\'
#out_dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'_fft\\'

#dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_csv\\'+dir_name[dir_i]+'\\'
#out_dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_csv\\'+dir_name[dir_i]+'_fft\\'

#dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_finger_csv\\'+dir_name[dir_i]+'\\'
#out_dir_path = 'C:\\Users\\student\\Documents\\data\\haptics_finger_csv\\'+dir_name[dir_i]+'_fft\\'

out_dir_path = 'C:\\Users\\student\\Documents\\data\\'+dir_name[dir_i]+'_fft2\\'

#--------------------------------------------------------------------------------------------#
                                    # 振動データの出力先を指定--end
#--------------------------------------------------------------------------------------------#

files = os.listdir(dir_path)

if os.path.exists(out_dir_path) is False:
    os.makedirs(out_dir_path)
    print("make dir")

#count = 0
for file in files:
    print("file:{}".format(file))
#    if count > 0:
#        break
#    count+=1

    data = pd.read_csv(dir_path+file,header=None)

    acc_list = [[], [], []]
    acc_list[0].extend(data.loc[0])
    acc_list[1].extend(data.loc[1])
    acc_list[2].extend(data.loc[2])

 
    min_acc = len(acc_list[0])
    for i in range(0,3):
        if min_acc > len(acc_list[i]): 
            min_acc = len(acc_list[i])
    print("min_acc:{}".format(min_acc))
#    lest = len(min_acc) % 3
#    print("lest:{}".format(lest))        
    
    if min_acc < 900:
        continue
    
    print("0:{}".format(len(acc_list[0])))
    print("1:{}".format(len(acc_list[1])))
    print("2:{}".format(len(acc_list[2])))

    acc_list[0] = acc_list[0][0:min_acc]  
    acc_list[1] = acc_list[1][0:min_acc]                    
    acc_list[2] = acc_list[2][0:min_acc]  
 

################################################################################
#                                   fft
################################################################################

#    fs = 334 # Sampling rate
    L = len(acc_list[0]) # Signal length
    
    # 窓関数
    win = hamming(L)
#    print("win:{}".format(win))
    
    # 標本化定理
    # フーリエ変換の最初に格納されているデータは使用できないため、1範囲を広げる

#    idx_start = 2    
    idx_start = 0
    half_L = int(L/2)
    #half_L = int(L / 2 + 1)
    #half_L = int(L / 2 + idx_start)
    
#    フーリエ変換
    spectrum = []

    for i in range(0,3):
        spectrum.append(fft(np.array(acc_list[i])*win))

# 標本化定理を適応し、周波数の半分のデータを取得する
    half_spectrum = []
    for i in range(0,3):
#        half_spectrum.append(abs(np.array(spectrum[i][1:half_L])))
        half_spectrum.append(abs(np.array(spectrum[i][idx_start:half_L])))


#    # 横軸周波数
    fs = 334 #5s1670, 334hz
    freqList = fftfreq(L , 1/fs)
#    #half_freqList = freqList[1:half_L]
    half_freqList = freqList[idx_start:half_L]
#
#
#    # フーリエ変換後の図を表示
    fig = plt.figure(figsize=(10,8))
    # openのFFT値を確認
    fig.add_subplot(411)
    plt.plot(half_freqList, half_spectrum[0])
    plt.xlim([0,fs/2])
#    plt.ylim([0,1024])
    
    fig.add_subplot(412)
    plt.plot(half_freqList, half_spectrum[1])
    plt.xlim([0,fs/2])
#    plt.ylim([0,512])
    
    fig.add_subplot(413)
    plt.plot(half_freqList, half_spectrum[2])
    plt.xlim([0,fs/2])
#    plt.ylim([0,512])
            

    
    # ここにデータとトレーニングデータを付け加える
    data = pd.DataFrame({'x':half_spectrum[0],
                         'y':half_spectrum[1],
                         'z':half_spectrum[2]}).T
                         
    # csvファイルに書き出し
#    half_freqList = list(half_freqList)
#    half_freqList.insert(0,"axis / hz")
#   
    # 保存
#    fileName = out_dir_path + file_name[file_i] + file
    fileName = out_dir_path + file
    print(fileName)
    data.to_csv(fileName, mode='w',header=None, index=None)
#    data.to_csv(fileName, mode='w',index_label=half_freqList) 

         