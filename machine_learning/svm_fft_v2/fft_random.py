# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:46:28 2016

@author: student
"""

import pandas as pd
import numpy as np
import os
from scipy import hamming
from scipy.fftpack import fft





################################################################################
#                               データの前処理
################################################################################

# データ取得
open1 = pd.read_csv('C:/Users/student/Documents/door-open/open1.csv')
open2 = pd.read_csv('C:/Users/student/Documents/door-open/open2.csv')
open3 = pd.read_csv('C:/Users/student/Documents/door-open/open3.csv')
open4 = pd.read_csv('C:/Users/student/Documents/door-open/open4.csv')

dondon1 = pd.read_csv('C:/Users/student/Documents/dondon/dondon1.csv')
dondon2 = pd.read_csv('C:/Users/student/Documents/dondon/dondon2.csv')
dondon3 = pd.read_csv('C:/Users/student/Documents/dondon/dondon3.csv')
dondon4 = pd.read_csv('C:/Users/student/Documents/dondon/dondon4.csv')


# 列名追加
open1.columns = ['index','x', 'y', 'z']
open2.columns = ['index','x', 'y', 'z']
open3.columns = ['index','x', 'y', 'z']
open4.columns = ['index','x', 'y', 'z']

dondon1.columns = ['index','x', 'y', 'z']
dondon2.columns = ['index','x', 'y', 'z']
dondon3.columns = ['index','x', 'y', 'z']
dondon4.columns = ['index','x', 'y', 'z']

# 列の削除
open1 = open1.drop('index', axis=1)
open2 = open2.drop('index', axis=1)
open3 = open3.drop('index', axis=1)
open4 = open4.drop('index', axis=1)

dondon1 = dondon1.drop('index', axis=1)
dondon2 = dondon2.drop('index', axis=1)
dondon3 = dondon3.drop('index', axis=1)
dondon4 = dondon4.drop('index', axis=1)

# データの長さを求める
open1_length = len(open1)
open2_length = len(open2)
open3_length = len(open3)
open4_length = len(open4)

dondon1_length = len(dondon1)
dondon2_length = len(dondon2)
dondon3_length = len(dondon3)
dondon4_length = len(dondon4)

################################################################################
#                               5秒間を切り出す
################################################################################
split_second = 5000
a_split = 200
b_split = 500


# 商を求める
open1_quotient = int(open1_length / split_second)
open2_quotient = int(open2_length / split_second)
open3_quotient = int(open3_length / split_second)
open4_quotient = int(open4_length / split_second)

dondon1_quotient = int(dondon1_length / split_second)
dondon2_quotient = int(dondon2_length / split_second)
dondon3_quotient = int(dondon3_length / split_second)
dondon4_quotient = int(dondon4_length / split_second)

# 商の最小値を求める
quotient_length = np.array((open1_quotient, open2_quotient, open3_quotient, open4_quotient,
                            dondon1_quotient, dondon2_quotient, dondon3_quotient, dondon4_quotient))
quotient_min = quotient_length.min()
# データ削減
quotient_min = quotient_min
training_upper_num = int(quotient_min * 0.7)
test_upper_num = quotient_min - training_upper_num 

################################################################################
################################################################################



################################################################################
#                                   SVM
################################################################################

    
# トレーニングデータとテストデータを ７:３ に分割
#training_datas_quotient_num = int(quotient_min * 0.7)
#test_labels_quotient_num = int(quotient_min - training_datas_quotient_num)

#training_upper = int(split_second * training_datas_quotient_num)   
training_upper = split_second * training_upper_num
test_upper = split_second * quotient_min
#test_num = test_upper - training_upper

start = 0 
stop = split_second
count = 0
k = 1
while True:
    k += 1
    count += 1
   
    if stop > training_upper:
        break

#    print('学習回数:%s' % count)
    
    training_open1 = open1[start : stop]
    training_open2 = open2[start : stop]
    training_open3 = open3[start : stop]
    training_open4 = open4[start : stop]
    
    training_dondon1 = dondon1[start : stop]
    training_dondon2 = dondon2[start : stop]
    training_dondon3 = dondon3[start : stop]
    training_dondon4 = dondon4[start : stop]
#################################################################################
#                                   fft
#################################################################################
    
    fs = 1024 # Sampling rate
    L = 5000 # Signal length
    #NUMBER = 20
    
    
    # 全部足す
    #sin_open1 = training_open1
    x_sin_open1 = training_open1['x']
    y_sin_open1 = training_open1['y']
    z_sin_open1 = training_open1['z']
    
    x_sin_open2 = training_open2['x']
    y_sin_open2 = training_open2['y']
    z_sin_open2 = training_open2['z']
    
    x_sin_open3 = training_open3['x']
    y_sin_open3 = training_open3['y']
    z_sin_open3 = training_open3['z']
    
    x_sin_open4 = training_open4['x']
    y_sin_open4 = training_open4['y']
    z_sin_open4 = training_open4['z']
        
    x_sin_dondon1 = training_dondon1['x']
    y_sin_dondon1 = training_dondon1['y']
    z_sin_dondon1 = training_dondon1['z']
    
    x_sin_dondon2 = training_dondon2['x']
    y_sin_dondon2 = training_dondon2['y']
    z_sin_dondon2 = training_dondon2['z']
    
    x_sin_dondon3 = training_dondon3['x']
    y_sin_dondon3 = training_dondon3['y']
    z_sin_dondon3 = training_dondon3['z']
    
    x_sin_dondon4 = training_dondon4['x']
    y_sin_dondon4 = training_dondon4['y']
    z_sin_dondon4 = training_dondon4['z']
    
    # 窓関数
    win = hamming(L)
    
    # 標本化定理
    # フーリエ変換の最初に格納されているデータは使用できないため、1範囲を広げる
    half_L = int(L / 2 + 1)
    
    
    #    フーリエ変換
    #spectrum_nw_open1 = fft(sin_open1) # 窓関数なし
    x_spectrum_open1 = fft(x_sin_open1 * win) # 窓関数あり
    y_spectrum_open1 = fft(y_sin_open1 * win) # 窓関数あり
    z_spectrum_open1 = fft(z_sin_open1 * win) # 窓関数あり
    
    x_spectrum_open2 = fft(x_sin_open2 * win) # 窓関数あり
    y_spectrum_open2 = fft(y_sin_open2 * win) # 窓関数あり
    z_spectrum_open2 = fft(z_sin_open2 * win) # 窓関数あり
    
    x_spectrum_open3 = fft(x_sin_open3 * win) # 窓関数あり
    y_spectrum_open3 = fft(y_sin_open3 * win) # 窓関数あり
    z_spectrum_open3 = fft(z_sin_open3 * win) # 窓関数あり
    
    x_spectrum_open4 = fft(x_sin_open4 * win) # 窓関数あり
    y_spectrum_open4 = fft(y_sin_open4 * win) # 窓関数あり
    z_spectrum_open4 = fft(z_sin_open4 * win) # 窓関数あり
    
    # 標本化定理を適応し、周波数の半分のデータを取得する
    #    half_spectrum_nw_open1 = abs(spectrum_nw_open1[1:half_L])
    x_half_spectrum_open1 = abs(x_spectrum_open1[1:half_L])
    y_half_spectrum_open1 = abs(y_spectrum_open1[1:half_L])
    z_half_spectrum_open1 = abs(z_spectrum_open1[1:half_L])
    
    x_half_spectrum_open2 = abs(x_spectrum_open2[1:half_L])
    y_half_spectrum_open2 = abs(y_spectrum_open2[1:half_L])
    z_half_spectrum_open2 = abs(z_spectrum_open2[1:half_L])
    
    x_half_spectrum_open3 = abs(x_spectrum_open3[1:half_L])
    y_half_spectrum_open3 = abs(y_spectrum_open3[1:half_L])
    z_half_spectrum_open3 = abs(z_spectrum_open3[1:half_L])
    
    x_half_spectrum_open4 = abs(x_spectrum_open4[1:half_L])
    y_half_spectrum_open4 = abs(y_spectrum_open4[1:half_L])
    z_half_spectrum_open4 = abs(z_spectrum_open4[1:half_L])  
    
    #    spectrum_nw_dondon1 = fft(sin_dondon1) # 窓関数なし
    #    フーリエ変換
    x_spectrum_dondon1 = fft(x_sin_dondon1 * win) # 窓関数あり
    y_spectrum_dondon1 = fft(y_sin_dondon1 * win) # 窓関数あり
    z_spectrum_dondon1 = fft(z_sin_dondon1 * win) # 窓関数あり
    
    x_spectrum_dondon2 = fft(x_sin_dondon2 * win) # 窓関数あり
    y_spectrum_dondon2 = fft(y_sin_dondon2 * win) # 窓関数あり
    z_spectrum_dondon2 = fft(z_sin_dondon2 * win) # 窓関数あり
    
    x_spectrum_dondon3 = fft(x_sin_dondon3 * win) # 窓関数あり
    y_spectrum_dondon3 = fft(y_sin_dondon3 * win) # 窓関数あり
    z_spectrum_dondon3 = fft(z_sin_dondon3 * win) # 窓関数あり
    
    x_spectrum_dondon4 = fft(x_sin_dondon4 * win) # 窓関数あり
    y_spectrum_dondon4 = fft(y_sin_dondon4 * win) # 窓関数あり
    z_spectrum_dondon4 = fft(z_sin_dondon4 * win) # 窓関数あり
    #    half_spectrum_nw_dondon1 = abs(spectrum_nw_dondon1[1:half_L])
    
    
    # 標本化定理を適応し、周波数の半分のデータを取得する
    x_half_spectrum_dondon1 = abs(x_spectrum_dondon1[1:half_L])
    y_half_spectrum_dondon1 = abs(y_spectrum_dondon1[1:half_L])
    z_half_spectrum_dondon1 = abs(z_spectrum_dondon1[1:half_L])
    
    x_half_spectrum_dondon2 = abs(x_spectrum_dondon2[1:half_L])
    y_half_spectrum_dondon2 = abs(y_spectrum_dondon2[1:half_L])
    z_half_spectrum_dondon2 = abs(z_spectrum_dondon2[1:half_L])
        
    x_half_spectrum_dondon3 = abs(x_spectrum_dondon3[1:half_L])
    y_half_spectrum_dondon3 = abs(y_spectrum_dondon3[1:half_L])
    z_half_spectrum_dondon3 = abs(z_spectrum_dondon3[1:half_L])
    
    x_half_spectrum_dondon4 = abs(x_spectrum_dondon4[1:half_L])
    y_half_spectrum_dondon4 = abs(y_spectrum_dondon4[1:half_L])
    z_half_spectrum_dondon4 = abs(z_spectrum_dondon4[1:half_L])
    
##################################################################################
#                               学習データ（dondon初期値）
##################################################################################
    
    
#    print("##### dondon #####")
    
    t=0
    j=0
    s=0
    n=a_split
    
    
    x_dondon1 = x_half_spectrum_dondon1[s:n].sum()
    y_dondon1 = y_half_spectrum_dondon1[s:n].sum()
    z_dondon1 = z_half_spectrum_dondon1[s:n].sum()
    
    x_dondon2 = x_half_spectrum_dondon2[s:n].sum()
    y_dondon2 = y_half_spectrum_dondon2[s:n].sum()
    z_dondon2 = z_half_spectrum_dondon2[s:n].sum()
    
    x_dondon3 = x_half_spectrum_dondon3[s:n].sum()
    y_dondon3 = y_half_spectrum_dondon3[s:n].sum()
    z_dondon3 = z_half_spectrum_dondon3[s:n].sum()
    
    x_dondon4 = x_half_spectrum_dondon4[s:n].sum()
    y_dondon4 = y_half_spectrum_dondon4[s:n].sum()
    z_dondon4 = z_half_spectrum_dondon4[s:n].sum()
    
    
    con_dondon1 = pd.DataFrame({'x': x_dondon1,
                                'y': y_dondon1,
                                'z': z_dondon1},index=['dondon1'])
    
    con_dondon2 = pd.DataFrame({'x': x_dondon2,
                                'y': y_dondon2,
                                'z': z_dondon2},index=['dondon2'])
    
    con_dondon3 = pd.DataFrame({'x': x_dondon3,
                                'y': y_dondon3,
                                'z': z_dondon3},index=['dondon3'])
    
    con_dondon4 = pd.DataFrame({'x': x_dondon4,
                                'y': y_dondon4,
                                'z': z_dondon4},index=['dondon4'])
                                         
    training_label1 = pd.DataFrame({'label': 0},index=['label'])
    training_label2 = pd.DataFrame({'label': 0},index=['label'])
    training_label3 = pd.DataFrame({'label': 0},index=['label'])
    training_label4 = pd.DataFrame({'label': 0},index=['label'])
     

                                   
    half_spectrum_dondon1 = np.hstack((con_dondon1, training_label1))
    half_spectrum_dondon2 = np.hstack((con_dondon2, training_label2))
    half_spectrum_dondon3 = np.hstack((con_dondon3, training_label3))
    half_spectrum_dondon4 = np.hstack((con_dondon4, training_label4))

    s=n;n+=a_split
    
    
##################################################################################
#                              学習データ（dondon）
##################################################################################
    a_count=0 
    while True:
        a_count += 1    
        if s >= 2500:
#            print("学習データdondon:%d" % a_count)
            break
        elif n <= 1000:
    
#            print('{0} → {1}'.format(s,n))
            x_dondon1 = x_half_spectrum_dondon1[s:n].sum()
            y_dondon1 = y_half_spectrum_dondon1[s:n].sum()
            z_dondon1 = z_half_spectrum_dondon1[s:n].sum()
    
            x_dondon2 = x_half_spectrum_dondon2[s:n].sum()
            y_dondon2 = y_half_spectrum_dondon2[s:n].sum()
            z_dondon2 = z_half_spectrum_dondon2[s:n].sum()
            
            x_dondon3 = x_half_spectrum_dondon3[s:n].sum()
            y_dondon3 = y_half_spectrum_dondon3[s:n].sum()
            z_dondon3 = z_half_spectrum_dondon3[s:n].sum()
            
            x_dondon4 = x_half_spectrum_dondon4[s:n].sum()
            y_dondon4 = y_half_spectrum_dondon4[s:n].sum()
            z_dondon4 = z_half_spectrum_dondon4[s:n].sum()
            
    
    
            spectrum_dondon1 = pd.DataFrame({'x': x_dondon1,
                                             'y': y_dondon1,
                                             'z': z_dondon1},index=['dondon1'])
    
            spectrum_dondon2 = pd.DataFrame({'x': x_dondon2,
                                             'y': y_dondon2,
                                             'z': z_dondon2},index=['dondon2'])
    
            spectrum_dondon3 = pd.DataFrame({'x': x_dondon3,
                                             'y': y_dondon3,
                                             'z': z_dondon3},index=['dondon3'])
                                             
            spectrum_dondon4 = pd.DataFrame({'x': x_dondon4,
                                             'y': y_dondon4,
                                             'z': z_dondon4},index=['dondon4'])
                                             
                                            
            spectrum_dondon1 = np.hstack((spectrum_dondon1, training_label1))
            spectrum_dondon2 = np.hstack((spectrum_dondon2, training_label2))
            spectrum_dondon3 = np.hstack((spectrum_dondon3, training_label3))
            spectrum_dondon4 = np.hstack((spectrum_dondon4, training_label4))

    
            half_spectrum_dondon1 = np.vstack((half_spectrum_dondon1, spectrum_dondon1))
            half_spectrum_dondon2 = np.vstack((half_spectrum_dondon2, spectrum_dondon2))
            half_spectrum_dondon3 = np.vstack((half_spectrum_dondon3, spectrum_dondon3))
            half_spectrum_dondon4 = np.vstack((half_spectrum_dondon4, spectrum_dondon4))

            t += 1
            s = n;n+=a_split        
        elif s >= 1000 and n <= 2500:
            if(j == 0):
                s=1000;n=s+b_split
#                print('####### a_split0~2a_split0 ######')
#            print('{0} → {1}'.format(s,n))
            x_spectrum_dondon1 = x_half_spectrum_dondon1[s:n].sum()
            y_spectrum_dondon1 = y_half_spectrum_dondon1[s:n].sum()
            z_spectrum_dondon1 = z_half_spectrum_dondon1[s:n].sum()
    
            x_spectrum_dondon2 = x_half_spectrum_dondon2[s:n].sum()
            y_spectrum_dondon2 = y_half_spectrum_dondon2[s:n].sum()
            z_spectrum_dondon2 = z_half_spectrum_dondon2[s:n].sum()
    
            x_spectrum_dondon3 = x_half_spectrum_dondon3[s:n].sum()
            y_spectrum_dondon3 = y_half_spectrum_dondon3[s:n].sum()
            z_spectrum_dondon3 = z_half_spectrum_dondon3[s:n].sum()
    
            x_spectrum_dondon4 = x_half_spectrum_dondon4[s:n].sum()
            y_spectrum_dondon4 = y_half_spectrum_dondon4[s:n].sum()
            z_spectrum_dondon4 = z_half_spectrum_dondon4[s:n].sum()  
            
    
            spectrum_dondon1 = pd.DataFrame({'x': x_spectrum_dondon1,
                                             'y': y_spectrum_dondon1,
                                             'z': z_spectrum_dondon1},index=['dondon1'])
    
            spectrum_dondon2 = pd.DataFrame({'x': x_spectrum_dondon2,
                                             'y': y_spectrum_dondon2,
                                             'z': z_spectrum_dondon2},index=['dondon2'])
            
            spectrum_dondon3 = pd.DataFrame({'x': x_spectrum_dondon3,
                                             'y': y_spectrum_dondon3,
                                             'z': z_spectrum_dondon3},index=['dondon3'])
    
            spectrum_dondon4 = pd.DataFrame({'x': x_spectrum_dondon4,
                                             'y': y_spectrum_dondon4,
                                             'z': z_spectrum_dondon4},index=['dondon4'])
                                        
            x_spectrum_dondon1 = np.hstack((spectrum_dondon1, training_label1))
            x_spectrum_dondon2 = np.hstack((spectrum_dondon2, training_label2))
            x_spectrum_dondon3 = np.hstack((spectrum_dondon3, training_label3))
            x_spectrum_dondon4 = np.hstack((spectrum_dondon4, training_label4))
    
    
            half_spectrum_dondon1 = np.vstack((half_spectrum_dondon1, x_spectrum_dondon1))
            half_spectrum_dondon2 = np.vstack((half_spectrum_dondon2, x_spectrum_dondon2))
            half_spectrum_dondon3 = np.vstack((half_spectrum_dondon3, x_spectrum_dondon3))
            half_spectrum_dondon4 = np.vstack((half_spectrum_dondon4, x_spectrum_dondon4))
            
            s=n; n+=b_split
            j += 1
        else:
            print('t:%d' % t)
            print('j:%d' % j)
            print('finish')
            break
    
    
    half_spectrum_dondon = np.vstack([half_spectrum_dondon1, half_spectrum_dondon2, half_spectrum_dondon3, half_spectrum_dondon4])
    

    
#    print("##### open #####")
    t=0
    j=0
    s=0
    n=a_split
    
################################################################################
#                                   学習データopen(初期化)
################################################################################
    x_open1 = x_half_spectrum_open1[s:n].sum()
    y_open1 = y_half_spectrum_open1[s:n].sum()
    z_open1 = z_half_spectrum_open1[s:n].sum()
    
    x_open2 = x_half_spectrum_open2[s:n].sum()
    y_open2 = y_half_spectrum_open2[s:n].sum()
    z_open2 = z_half_spectrum_open2[s:n].sum()
    
    x_open3 = x_half_spectrum_open3[s:n].sum()
    y_open3 = y_half_spectrum_open3[s:n].sum()
    z_open3 = z_half_spectrum_open3[s:n].sum()
    
    x_open4 = x_half_spectrum_open4[s:n].sum()
    y_open4 = y_half_spectrum_open4[s:n].sum()
    z_open4 = z_half_spectrum_open4[s:n].sum()
    
    
    con_open1 = pd.DataFrame({'x': x_open1,
                              'y': y_open1,
                              'z': z_open1},index=['open1'])
    
    con_open2 = pd.DataFrame({'x': x_open2,
                              'y': y_open2,
                              'z': z_open2},index=['open2'])
    
    con_open3 = pd.DataFrame({'x': x_open3,
                              'y': y_open3,
                              'z': z_open3},index=['open3'])
    
    con_open4 = pd.DataFrame({'x': x_open4,
                              'y': y_open4,
                              'z': z_open4},index=['open4'])
                                     
    training_label1 = pd.DataFrame({'label': 1},index=['label'])
    training_label2 = pd.DataFrame({'label': 1},index=['label'])
    training_label3= pd.DataFrame({'label': 1},index=['label'])
    training_label4 = pd.DataFrame({'label': 1},index=['label'])
                               
    half_spectrum_open1 = np.hstack((con_open1, training_label1))
    half_spectrum_open2 = np.hstack((con_open2, training_label2))
    half_spectrum_open3 = np.hstack((con_open3, training_label3))
    half_spectrum_open4 = np.hstack((con_open4, training_label4))

    s=n;n+=a_split

##################################################################################
#                               学習データ（open）
##################################################################################
    a_count=0
    while True:
        a_count+=1
        if s >= 2500:
#            print("学習データopen:%d" % a_count)

            break
        elif n <= 1000:
             
#            print('{0} → {1}'.format(s,n))
            x_open1 = x_half_spectrum_open1[s:n].sum()
            y_open1 = y_half_spectrum_open1[s:n].sum()
            z_open1 = z_half_spectrum_open1[s:n].sum()
    
            x_open2 = x_half_spectrum_open2[s:n].sum()
            y_open2 = y_half_spectrum_open2[s:n].sum()
            z_open2 = z_half_spectrum_open2[s:n].sum()
            
            x_open3 = x_half_spectrum_open3[s:n].sum()
            y_open3 = y_half_spectrum_open3[s:n].sum()
            z_open3 = z_half_spectrum_open3[s:n].sum()
            
            x_open4 = x_half_spectrum_open4[s:n].sum()
            y_open4 = y_half_spectrum_open4[s:n].sum()
            z_open4 = z_half_spectrum_open4[s:n].sum()
    
    
            spectrum_open1 = pd.DataFrame({'x': x_open1,
                                           'y': y_open1,
                                           'z': z_open1},index=['open1'])
    
            spectrum_open2 = pd.DataFrame({'x': x_open2,
                                           'y': y_open2,
                                           'z': z_open2},index=['open2'])
    
            spectrum_open3 = pd.DataFrame({'x': x_open3,
                                           'y': y_open3,
                                           'z': z_open3},index=['open3'])
                                             
            spectrum_open4 = pd.DataFrame({'x': x_open4,
                                           'y': y_open4,
                                           'z': z_open4},index=['open4'])
                                             
                                            
            spectrum_open1 = np.hstack((spectrum_open1, training_label1))
            spectrum_open2 = np.hstack((spectrum_open2, training_label2))
            spectrum_open3 = np.hstack((spectrum_open3, training_label3))
            spectrum_open4 = np.hstack((spectrum_open4, training_label4))
    
            half_spectrum_open1 = np.vstack((half_spectrum_open1, spectrum_open1))
            half_spectrum_open2 = np.vstack((half_spectrum_open2, spectrum_open2))
            half_spectrum_open3 = np.vstack((half_spectrum_open3, spectrum_open3))
            half_spectrum_open4 = np.vstack((half_spectrum_open4, spectrum_open4))

    
            t += 1
            s = n
            n = n + a_split        
        elif s >= 1000 and n <= 2500:
            if(j == 0):
                s=1000;n=s+b_split
#                print('####### a_split0~2a_split0 ######')
#            print('{0} → {1}'.format(s,n))
            x_spectrum_open1 = x_half_spectrum_open1[s:n].sum()
            y_spectrum_open1 = y_half_spectrum_open1[s:n].sum()
            z_spectrum_open1 = z_half_spectrum_open1[s:n].sum()
    
            x_spectrum_open2 = x_half_spectrum_open2[s:n].sum()
            y_spectrum_open2 = y_half_spectrum_open2[s:n].sum()
            z_spectrum_open2 = z_half_spectrum_open2[s:n].sum()
    
            x_spectrum_open3 = x_half_spectrum_open3[s:n].sum()
            y_spectrum_open3 = y_half_spectrum_open3[s:n].sum()
            z_spectrum_open3 = z_half_spectrum_open3[s:n].sum()
    
            x_spectrum_open4 = x_half_spectrum_open4[s:n].sum()
            y_spectrum_open4 = y_half_spectrum_open4[s:n].sum()
            z_spectrum_open4 = z_half_spectrum_open4[s:n].sum()  
            
    
            spectrum_open1 = pd.DataFrame({'x': x_spectrum_open1,
                                           'y': y_spectrum_open1,
                                           'z': z_spectrum_open1},index=['open1'])
    
            spectrum_open2 = pd.DataFrame({'x': x_spectrum_open2,
                                           'y': y_spectrum_open2,
                                           'z': z_spectrum_open2},index=['open2'])
            
            spectrum_open3 = pd.DataFrame({'x': x_spectrum_open3,
                                           'y': y_spectrum_open3,
                                           'z': z_spectrum_open3},index=['open3'])
    
            spectrum_open4 = pd.DataFrame({'x': x_spectrum_open4,
                                           'y': y_spectrum_open4,
                                           'z': z_spectrum_open4},index=['open4'])
                                        
            x_spectrum_open1 = np.hstack((spectrum_open1, training_label1))
            x_spectrum_open2 = np.hstack((spectrum_open2, training_label2))
            x_spectrum_open3 = np.hstack((spectrum_open3, training_label3))
            x_spectrum_open4 = np.hstack((spectrum_open4, training_label4))
    
            half_spectrum_open1 = np.vstack((half_spectrum_open1, x_spectrum_open1))
            half_spectrum_open2 = np.vstack((half_spectrum_open2, x_spectrum_open2))
            half_spectrum_open3 = np.vstack((half_spectrum_open3, x_spectrum_open3))
            half_spectrum_open4 = np.vstack((half_spectrum_open4, x_spectrum_open4))

    
            
            s = n
            n+=b_split
            j += 1
        else:
            print('t:%d' % t)
            print('j:%d' % j)
            print('finish')
            break

    half_spectrum_open = np.vstack([half_spectrum_open1, half_spectrum_open2, half_spectrum_open3, half_spectrum_open4])
##################################################################################
#                               トレーニングデータ書き込み
##################################################################################
    half_spectrum = np.vstack([half_spectrum_open, half_spectrum_dondon]) 
    print("学習 : %d" % len(half_spectrum))

    training = pd.DataFrame(half_spectrum)                      
            # csvファイルに書き出し
    fileName = "fft_training.csv"
    if os.path.exists(fileName) and count==1:
        os.remove(fileName)
    training.to_csv(fileName, mode='a',header=None, index=None)
        
    start = stop
    stop = stop + split_second

    


##################################################################################
#                               テストデータ
##################################################################################

start = training_upper
stop = training_upper + split_second
count = 0
k = 1
while True:
    k += 1
    count += 1
    
    if stop > test_upper:
#        print("テストデータ:%d" % count)
        break
#    print('テストデータ回数:%s' % count)
    test_open1 = open1[start : stop]
    test_open2 = open2[start : stop]
    test_open3 = open3[start : stop]
    test_open4 = open4[start : stop]
    
    test_dondon1 = dondon1[start : stop]
    test_dondon2 = dondon2[start : stop]
    test_dondon3 = dondon3[start : stop]
    test_dondon4 = dondon4[start : stop]
#################################################################################
#                                   fft
#################################################################################
    
    fs = 1000 # Sampling rate
    L = 5000 # Signal length
    #NUMBER = 20
    
    
    # 全部足す
    #sin_open1 = test_open1
    x_sin_open1 = test_open1['x']
    y_sin_open1 = test_open1['y']
    z_sin_open1 = test_open1['z']
    
    x_sin_open2 = test_open2['x']
    y_sin_open2 = test_open2['y']
    z_sin_open2 = test_open2['z']
    
    x_sin_open3 = test_open3['x']
    y_sin_open3 = test_open3['y']
    z_sin_open3 = test_open3['z']
    
    x_sin_open4 = test_open4['x']
    y_sin_open4 = test_open4['y']
    z_sin_open4 = test_open4['z']
        
    x_sin_dondon1 = test_dondon1['x']
    y_sin_dondon1 = test_dondon1['y']
    z_sin_dondon1 = test_dondon1['z']
    
    x_sin_dondon2 = test_dondon2['x']
    y_sin_dondon2 = test_dondon2['y']
    z_sin_dondon2 = test_dondon2['z']
    
    x_sin_dondon3 = test_dondon3['x']
    y_sin_dondon3 = test_dondon3['y']
    z_sin_dondon3 = test_dondon3['z']
    
    x_sin_dondon4 = test_dondon4['x']
    y_sin_dondon4 = test_dondon4['y']
    z_sin_dondon4 = test_dondon4['z']
    
    # 窓関数
    win = hamming(L)
    
    # 標本化定理
    # フーリエ変換の最初に格納されているデータは使用できないため、1範囲を広げる
    half_L = int(L / 2 + 1)
    
    # フーリエ変換
    x_spectrum_open1 = fft(x_sin_open1 * win) # 窓関数あり
    y_spectrum_open1 = fft(y_sin_open1 * win) # 窓関数あり
    z_spectrum_open1 = fft(z_sin_open1 * win) # 窓関数あり
    
    x_spectrum_open2 = fft(x_sin_open2 * win) # 窓関数あり
    y_spectrum_open2 = fft(y_sin_open2 * win) # 窓関数あり
    z_spectrum_open2 = fft(z_sin_open2 * win) # 窓関数あり
    
    x_spectrum_open3 = fft(x_sin_open3 * win) # 窓関数あり
    y_spectrum_open3 = fft(y_sin_open3 * win) # 窓関数あり
    z_spectrum_open3 = fft(z_sin_open3 * win) # 窓関数あり
    
    x_spectrum_open4 = fft(x_sin_open4 * win) # 窓関数あり
    y_spectrum_open4 = fft(y_sin_open4 * win) # 窓関数あり
    z_spectrum_open4 = fft(z_sin_open4 * win) # 窓関数あり
    
    # 標本化定理を適応し、周波数の半分のデータを取得する
    #    half_spectrum_nw_open1 = abs(spectrum_nw_open1[1:half_L])
    x_half_spectrum_open1 = abs(x_spectrum_open1[1:half_L])
    y_half_spectrum_open1 = abs(y_spectrum_open1[1:half_L])
    z_half_spectrum_open1 = abs(z_spectrum_open1[1:half_L])
    
    x_half_spectrum_open2 = abs(x_spectrum_open2[1:half_L])
    y_half_spectrum_open2 = abs(y_spectrum_open2[1:half_L])
    z_half_spectrum_open2 = abs(z_spectrum_open2[1:half_L])
    
    x_half_spectrum_open3 = abs(x_spectrum_open3[1:half_L])
    y_half_spectrum_open3 = abs(y_spectrum_open3[1:half_L])
    z_half_spectrum_open3 = abs(z_spectrum_open3[1:half_L])
    
    x_half_spectrum_open4 = abs(x_spectrum_open4[1:half_L])
    y_half_spectrum_open4 = abs(y_spectrum_open4[1:half_L])
    z_half_spectrum_open4 = abs(z_spectrum_open4[1:half_L])  
    
    #    spectrum_nw_dondon1 = fft(sin_dondon1) # 窓関数なし
    #    フーリエ変換
    x_spectrum_dondon1 = fft(x_sin_dondon1 * win) # 窓関数あり
    y_spectrum_dondon1 = fft(y_sin_dondon1 * win) # 窓関数あり
    z_spectrum_dondon1 = fft(z_sin_dondon1 * win) # 窓関数あり
    
    x_spectrum_dondon2 = fft(x_sin_dondon2 * win) # 窓関数あり
    y_spectrum_dondon2 = fft(y_sin_dondon2 * win) # 窓関数あり
    z_spectrum_dondon2 = fft(z_sin_dondon2 * win) # 窓関数あり
    
    x_spectrum_dondon3 = fft(x_sin_dondon3 * win) # 窓関数あり
    y_spectrum_dondon3 = fft(y_sin_dondon3 * win) # 窓関数あり
    z_spectrum_dondon3 = fft(z_sin_dondon3 * win) # 窓関数あり
    
    x_spectrum_dondon4 = fft(x_sin_dondon4 * win) # 窓関数あり
    y_spectrum_dondon4 = fft(y_sin_dondon4 * win) # 窓関数あり
    z_spectrum_dondon4 = fft(z_sin_dondon4 * win) # 窓関数あり
    #    half_spectrum_nw_dondon1 = abs(spectrum_nw_dondon1[1:half_L])
    
    
    # 標本化定理を適応し、周波数の半分のデータを取得する
    x_half_spectrum_dondon1 = abs(x_spectrum_dondon1[1:half_L])
    y_half_spectrum_dondon1 = abs(y_spectrum_dondon1[1:half_L])
    z_half_spectrum_dondon1 = abs(z_spectrum_dondon1[1:half_L])
    
    x_half_spectrum_dondon2 = abs(x_spectrum_dondon2[1:half_L])
    y_half_spectrum_dondon2 = abs(y_spectrum_dondon2[1:half_L])
    z_half_spectrum_dondon2 = abs(z_spectrum_dondon2[1:half_L])
        
    x_half_spectrum_dondon3 = abs(x_spectrum_dondon3[1:half_L])
    y_half_spectrum_dondon3 = abs(y_spectrum_dondon3[1:half_L])
    z_half_spectrum_dondon3 = abs(z_spectrum_dondon3[1:half_L])
    
    x_half_spectrum_dondon4 = abs(x_spectrum_dondon4[1:half_L])
    y_half_spectrum_dondon4 = abs(y_spectrum_dondon4[1:half_L])
    z_half_spectrum_dondon4 = abs(z_spectrum_dondon4[1:half_L])
    
##################################################################################
#                               テストデータdondon(初期化)
##################################################################################
    
#    print("##### dondon #####")
    
    t=0
    j=0
    s = 0
    n = a_split
    
    
    x_dondon1 = x_half_spectrum_dondon1[s:n].sum()
    y_dondon1 = y_half_spectrum_dondon1[s:n].sum()
    z_dondon1 = z_half_spectrum_dondon1[s:n].sum()
    
    x_dondon2 = x_half_spectrum_dondon2[s:n].sum()
    y_dondon2 = y_half_spectrum_dondon2[s:n].sum()
    z_dondon2 = z_half_spectrum_dondon2[s:n].sum()
    
    x_dondon3 = x_half_spectrum_dondon3[s:n].sum()
    y_dondon3 = y_half_spectrum_dondon3[s:n].sum()
    z_dondon3 = z_half_spectrum_dondon3[s:n].sum()
    
    x_dondon4 = x_half_spectrum_dondon4[s:n].sum()
    y_dondon4 = y_half_spectrum_dondon4[s:n].sum()
    z_dondon4 = z_half_spectrum_dondon4[s:n].sum()
    
    
    con_dondon1 = pd.DataFrame({'x': x_dondon1,
                                'y': y_dondon1,
                                'z': z_dondon1},index=['dondon1'])
    
    con_dondon2 = pd.DataFrame({'x': x_dondon2,
                                'y': y_dondon2,
                                'z': z_dondon2},index=['dondon2'])
    
    con_dondon3 = pd.DataFrame({'x': x_dondon3,
                                'y': y_dondon3,
                                'z': z_dondon3},index=['dondon3'])
    
    con_dondon4 = pd.DataFrame({'x': x_dondon4,
                                'y': y_dondon4,
                                'z': z_dondon4},index=['dondon4'])
                                         
    test_label1 = pd.DataFrame({'label': 0,},index=['label'])
    test_label2 = pd.DataFrame({'label': 0,},index=['label'])
    test_label3 = pd.DataFrame({'label': 0,},index=['label'])
    test_label4 = pd.DataFrame({'label': 0,},index=['label'])

                                   
    half_spectrum_dondon1 = np.hstack((con_dondon1, test_label1))
    half_spectrum_dondon2 = np.hstack((con_dondon2, test_label2))
    half_spectrum_dondon3 = np.hstack((con_dondon3, test_label3))
    half_spectrum_dondon4 = np.hstack((con_dondon4, test_label4))

    
    s=n;n+=a_split
    
    
##################################################################################
#                               テストデータ(dondon)
##################################################################################
    a_count=0
    while True:
        a_count+=1
        if s >= 2500:
#            print("テストデータdondon:%d" % a_count)
            break
        elif n <= 1000:

#            print('{0} → {1}'.format(s,n))
            x_dondon1 = x_half_spectrum_dondon1[s:n].sum()
            y_dondon1 = y_half_spectrum_dondon1[s:n].sum()
            z_dondon1 = z_half_spectrum_dondon1[s:n].sum()
    
            x_dondon2 = x_half_spectrum_dondon2[s:n].sum()
            y_dondon2 = y_half_spectrum_dondon2[s:n].sum()
            z_dondon2 = z_half_spectrum_dondon2[s:n].sum()
            
            x_dondon3 = x_half_spectrum_dondon3[s:n].sum()
            y_dondon3 = y_half_spectrum_dondon3[s:n].sum()
            z_dondon3 = z_half_spectrum_dondon3[s:n].sum()
            
            x_dondon4 = x_half_spectrum_dondon4[s:n].sum()
            y_dondon4 = y_half_spectrum_dondon4[s:n].sum()
            z_dondon4 = z_half_spectrum_dondon4[s:n].sum()
            
    
    
            spectrum_dondon1 = pd.DataFrame({'x': x_dondon1,
                                             'y': y_dondon1,
                                             'z': z_dondon1},index=['dondon1'])
    
            spectrum_dondon2 = pd.DataFrame({'x': x_dondon2,
                                             'y': y_dondon2,
                                             'z': z_dondon2},index=['dondon2'])
    
            spectrum_dondon3 = pd.DataFrame({'x': x_dondon3,
                                             'y': y_dondon3,
                                             'z': z_dondon3},index=['dondon3'])
                                             
            spectrum_dondon4 = pd.DataFrame({'x': x_dondon4,
                                             'y': y_dondon4,
                                             'z': z_dondon4},index=['dondon4'])
                                             
                                            
            spectrum_dondon1 = np.hstack((spectrum_dondon1, test_label1))
            spectrum_dondon2 = np.hstack((spectrum_dondon2, test_label2))
            spectrum_dondon3 = np.hstack((spectrum_dondon3, test_label3))
            spectrum_dondon4 = np.hstack((spectrum_dondon4, test_label4))

    
            half_spectrum_dondon1 = np.vstack((half_spectrum_dondon1, spectrum_dondon1))
            half_spectrum_dondon2 = np.vstack((half_spectrum_dondon2, spectrum_dondon2))
            half_spectrum_dondon3 = np.vstack((half_spectrum_dondon3, spectrum_dondon3))
            half_spectrum_dondon4 = np.vstack((half_spectrum_dondon4, spectrum_dondon4))

    
            t += 1
            s = n; n+=a_split        
        elif s >= 1000 and n <= 2500:
            if(j == 0):
                s=1000;n=s+b_split
#                print('####### a_split0~2a_split0 ######')
#            print('{0} → {1}'.format(s,n))
            x_spectrum_dondon1 = x_half_spectrum_dondon1[s:n].sum()
            y_spectrum_dondon1 = y_half_spectrum_dondon1[s:n].sum()
            z_spectrum_dondon1 = z_half_spectrum_dondon1[s:n].sum()
    
            x_spectrum_dondon2 = x_half_spectrum_dondon2[s:n].sum()
            y_spectrum_dondon2 = y_half_spectrum_dondon2[s:n].sum()
            z_spectrum_dondon2 = z_half_spectrum_dondon2[s:n].sum()
    
            x_spectrum_dondon3 = x_half_spectrum_dondon3[s:n].sum()
            y_spectrum_dondon3 = y_half_spectrum_dondon3[s:n].sum()
            z_spectrum_dondon3 = z_half_spectrum_dondon3[s:n].sum()
    
            x_spectrum_dondon4 = x_half_spectrum_dondon4[s:n].sum()
            y_spectrum_dondon4 = y_half_spectrum_dondon4[s:n].sum()
            z_spectrum_dondon4 = z_half_spectrum_dondon4[s:n].sum()  
            
    
            spectrum_dondon1 = pd.DataFrame({'x': x_spectrum_dondon1,
                                             'y': y_spectrum_dondon1,
                                             'z': z_spectrum_dondon1},index=['dondon1'])
    
            spectrum_dondon2 = pd.DataFrame({'x': x_spectrum_dondon2,
                                             'y': y_spectrum_dondon2,
                                             'z': z_spectrum_dondon2},index=['dondon2'])
            
            spectrum_dondon3 = pd.DataFrame({'x': x_spectrum_dondon3,
                                             'y': y_spectrum_dondon3,
                                             'z': z_spectrum_dondon3},index=['dondon3'])
    
            spectrum_dondon4 = pd.DataFrame({'x': x_spectrum_dondon4,
                                             'y': y_spectrum_dondon4,
                                             'z': z_spectrum_dondon4},index=['dondon4'])
                                        
            x_spectrum_dondon1 = np.hstack((spectrum_dondon1, test_label1))
            x_spectrum_dondon2 = np.hstack((spectrum_dondon2, test_label2))
            x_spectrum_dondon3 = np.hstack((spectrum_dondon3, test_label3))
            x_spectrum_dondon4 = np.hstack((spectrum_dondon4, test_label4))

    
    
            half_spectrum_dondon1 = np.vstack((half_spectrum_dondon1, x_spectrum_dondon1))
            half_spectrum_dondon2 = np.vstack((half_spectrum_dondon2, x_spectrum_dondon2))
            half_spectrum_dondon3 = np.vstack((half_spectrum_dondon3, x_spectrum_dondon3))
            half_spectrum_dondon4 = np.vstack((half_spectrum_dondon4, x_spectrum_dondon4))

    
            
            s = n; n+=b_split
            j += 1
        else:
            print('t:%d' % t)
            print('j:%d' % j)
            print('finish')
            break
    
    
    half_spectrum_dondon = np.vstack([half_spectrum_dondon1, half_spectrum_dondon2, half_spectrum_dondon3, half_spectrum_dondon4])
    
    
##################################################################################
#                               テストデータopen(初期化)
##################################################################################

#    print("##### open #####")
    t=0
    j=0
    s=0
    n=a_split
    x_open1 = x_half_spectrum_open1[s:n].sum()
    y_open1 = y_half_spectrum_open1[s:n].sum()
    z_open1 = z_half_spectrum_open1[s:n].sum()
    
    x_open2 = x_half_spectrum_open2[s:n].sum()
    y_open2 = y_half_spectrum_open2[s:n].sum()
    z_open2 = z_half_spectrum_open2[s:n].sum()
    
    x_open3 = x_half_spectrum_open3[s:n].sum()
    y_open3 = y_half_spectrum_open3[s:n].sum()
    z_open3 = z_half_spectrum_open3[s:n].sum()
    
    x_open4 = x_half_spectrum_open4[s:n].sum()
    y_open4 = y_half_spectrum_open4[s:n].sum()
    z_open4 = z_half_spectrum_open4[s:n].sum()
    
    
    con_open1 = pd.DataFrame({'x': x_open1,
                              'y': y_open1,
                              'z': z_open1},index=['open1'])
    
    con_open2 = pd.DataFrame({'x': x_open2,
                              'y': y_open2,
                              'z': z_open2},index=['open2'])
    
    con_open3 = pd.DataFrame({'x': x_open3,
                              'y': y_open3,
                              'z': z_open3},index=['open3'])
    
    con_open4 = pd.DataFrame({'x': x_open4,
                              'y': y_open4,
                              'z': z_open4},index=['open4'])
                                     
    test_label1 = pd.DataFrame({'label': 1},index=['label'])
    test_label2 = pd.DataFrame({'label': 1},index=['label'])
    test_label3 = pd.DataFrame({'label': 1},index=['label'])
    test_label4 = pd.DataFrame({'label': 1},index=['label'])
                               
    half_spectrum_open1 = np.hstack((con_open1, test_label1))
    half_spectrum_open2 = np.hstack((con_open2, test_label2))
    half_spectrum_open3 = np.hstack((con_open3, test_label3))
    half_spectrum_open4 = np.hstack((con_open4, test_label4))


    s=n; n+=a_split
    
##################################################################################
#                               テストデータ(open)
##################################################################################
    a_count=0
    while True:
        a_count+=1
        if s >= 2500:
#            print("テストデータopen:%d" % a_count)
            break
        elif n <= 1000:
   
#            print('{0} → {1}'.format(s,n))
            x_open1 = x_half_spectrum_open1[s:n].sum()
            y_open1 = y_half_spectrum_open1[s:n].sum()
            z_open1 = z_half_spectrum_open1[s:n].sum()
    
            x_open2 = x_half_spectrum_open2[s:n].sum()
            y_open2 = y_half_spectrum_open2[s:n].sum()
            z_open2 = z_half_spectrum_open2[s:n].sum()
            
            x_open3 = x_half_spectrum_open3[s:n].sum()
            y_open3 = y_half_spectrum_open3[s:n].sum()
            z_open3 = z_half_spectrum_open3[s:n].sum()
            
            x_open4 = x_half_spectrum_open4[s:n].sum()
            y_open4 = y_half_spectrum_open4[s:n].sum()
            z_open4 = z_half_spectrum_open4[s:n].sum()
    
    
            spectrum_open1 = pd.DataFrame({'x': x_open1,
                                           'y': y_open1,
                                           'z': z_open1},index=['open1'])
    
            spectrum_open2 = pd.DataFrame({'x': x_open2,
                                           'y': y_open2,
                                           'z': z_open2},index=['open2'])
    
            spectrum_open3 = pd.DataFrame({'x': x_open3,
                                           'y': y_open3,
                                           'z': z_open3},index=['open3'])
                                             
            spectrum_open4 = pd.DataFrame({'x': x_open4,
                                           'y': y_open4,
                                           'z': z_open4},index=['open4'])
                                             
                                            
            spectrum_open1 = np.hstack((spectrum_open1, test_label1))
            spectrum_open2 = np.hstack((spectrum_open2, test_label2))
            spectrum_open3 = np.hstack((spectrum_open3, test_label3))
            spectrum_open4 = np.hstack((spectrum_open4, test_label4))

    
            half_spectrum_open1 = np.vstack((half_spectrum_open1, spectrum_open1))
            half_spectrum_open2 = np.vstack((half_spectrum_open2, spectrum_open2))
            half_spectrum_open3 = np.vstack((half_spectrum_open3, spectrum_open3))
            half_spectrum_open4 = np.vstack((half_spectrum_open4, spectrum_open4))

    
            t += 1
            s = n; n+=a_split        
        elif s >= 1000 and n <= 2500:
            if(j == 0):
                s=1000;n=s+b_split
#                print('####### a_split0~2a_split0 ######')
#            print('{0} → {1}'.format(s,n))
            x_spectrum_open1 = x_half_spectrum_open1[s:n].sum()
            y_spectrum_open1 = y_half_spectrum_open1[s:n].sum()
            z_spectrum_open1 = z_half_spectrum_open1[s:n].sum()
    
            x_spectrum_open2 = x_half_spectrum_open2[s:n].sum()
            y_spectrum_open2 = y_half_spectrum_open2[s:n].sum()
            z_spectrum_open2 = z_half_spectrum_open2[s:n].sum()
    
            x_spectrum_open3 = x_half_spectrum_open3[s:n].sum()
            y_spectrum_open3 = y_half_spectrum_open3[s:n].sum()
            z_spectrum_open3 = z_half_spectrum_open3[s:n].sum()
    
            x_spectrum_open4 = x_half_spectrum_open4[s:n].sum()
            y_spectrum_open4 = y_half_spectrum_open4[s:n].sum()
            z_spectrum_open4 = z_half_spectrum_open4[s:n].sum()  
            
    
            spectrum_open1 = pd.DataFrame({'x': x_spectrum_open1,
                                           'y': y_spectrum_open1,
                                           'z': z_spectrum_open1},index=['open1'])
    
            spectrum_open2 = pd.DataFrame({'x': x_spectrum_open2,
                                           'y': y_spectrum_open2,
                                           'z': z_spectrum_open2},index=['open2'])
            
            spectrum_open3 = pd.DataFrame({'x': x_spectrum_open3,
                                           'y': y_spectrum_open3,
                                           'z': z_spectrum_open3},index=['open3'])
    
            spectrum_open4 = pd.DataFrame({'x': x_spectrum_open4,
                                           'y': y_spectrum_open4,
                                           'z': z_spectrum_open4},index=['open4'])
                                        
            x_spectrum_open1 = np.hstack((spectrum_open1, test_label1))
            x_spectrum_open2 = np.hstack((spectrum_open2, test_label2))
            x_spectrum_open3 = np.hstack((spectrum_open3, test_label3))
            x_spectrum_open4 = np.hstack((spectrum_open4, test_label4))

    
            half_spectrum_open1 = np.vstack((half_spectrum_open1, x_spectrum_open1))
            half_spectrum_open2 = np.vstack((half_spectrum_open2, x_spectrum_open2))
            half_spectrum_open3 = np.vstack((half_spectrum_open3, x_spectrum_open3))
            half_spectrum_open4 = np.vstack((half_spectrum_open4, x_spectrum_open4))

    
            
            s = n
            n+=b_split
            j += 1
        else:
            print('t:%d' % t)
            print('j:%d' % j)
            print('finish')
            break
    

    half_spectrum_open = np.vstack([half_spectrum_open1, half_spectrum_open2, half_spectrum_open3, half_spectrum_open4])
##################################################################################
#                               ファイル書き出し
##################################################################################

    half_spectrum = np.vstack([half_spectrum_open, half_spectrum_dondon])
    print("テスト : %d" % len(half_spectrum))

    test = pd.DataFrame(half_spectrum)                      
            # csvファイルに書き出し
    fileName = "fft_test.csv"
    if os.path.exists(fileName) and count==1:
        os.remove(fileName)
    test.to_csv(fileName, mode='a',header=None, index=None)
        
        
    #print('学習モデル：%s' % svm_fit)
        
    start = stop
    stop = stop + split_second
