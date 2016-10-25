# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 22:32:05 2016

@author: student
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 13:28:52 2016

@author: student
"""


import pandas as pd
import numpy as np
import os
#from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn import svm
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import csv
from scipy import arange, hamming, sin, pi
from scipy.fftpack import fft, ifft, fftfreq
from matplotlib import pylab as pl
import numpy as np
import math #切り捨てのときに使用




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
start = 0
stop = split_second
roop_count = 1

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
quotient_min = quotient_min - 28

################################################################################
################################################################################



################################################################################
#                                   SVM
################################################################################

    
# トレーニングデータとテストデータを ７:３ に分割
training_datas_quotient_num = int(quotient_min * 0.7)
#test_labels_quotient_num = int(quotient_min - training_datas_quotient_num)

training_num = int(split_second * training_datas_quotient_num)   
test_upper = int(split_second * quotient_min)
test_num = test_upper - training_num    

#print(svm)

# トレーニングデータとトレーニングラベル
start = 0 
stop = split_second
i = 1
while True:
    i += 1
    #print(i)
    if stop > training_num:
        break
    
    training_open1 = open1[start : stop]
    training_open2 = open2[start : stop]
    training_open3 = open3[start : stop]
    training_open4 = open4[start : stop]
    
    training_dondon1 = dondon1[start : stop]
    training_dondon2 = dondon2[start : stop]
    training_dondon3 = dondon3[start : stop]
    training_dondon4 = dondon4[start : stop]

################################################################################
#                                   fft
################################################################################

    fs = 1000 # Sampling rate
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
################################################################################
################################################################################

# データと同じ長さのラベルを付ける
    training_labels_open1 = np.zeros(len(x_half_spectrum_open1))
    training_labels_open2 = np.zeros(len(x_half_spectrum_open2))
    training_labels_open3 = np.zeros(len(x_half_spectrum_open3))
    training_labels_open4 = np.zeros(len(x_half_spectrum_open4))

    training_labels_dondon1 = np.ones(len(x_half_spectrum_dondon1))
    training_labels_dondon2 = np.ones(len(x_half_spectrum_dondon2))
    training_labels_dondon3 = np.ones(len(x_half_spectrum_dondon3))
    training_labels_dondon4 = np.ones(len(x_half_spectrum_dondon4))
    
    
# データ結合   
    x_training_datas = np.hstack((x_half_spectrum_open1,
                                  x_half_spectrum_open2,
                                  x_half_spectrum_open3,
                                  x_half_spectrum_open4,
                                  x_half_spectrum_dondon1,
                                  x_half_spectrum_dondon2,
                                  x_half_spectrum_dondon3,
                                  x_half_spectrum_dondon4
                                  ))
    
    y_training_datas = np.hstack((y_half_spectrum_open1,
                                  y_half_spectrum_open2,
                                  y_half_spectrum_open3,
                                  y_half_spectrum_open4,
                                  y_half_spectrum_dondon1,
                                  y_half_spectrum_dondon2,
                                  y_half_spectrum_dondon3,
                                  y_half_spectrum_dondon4
                                  ))
    
    z_training_datas = np.hstack((z_half_spectrum_open1,
                                  z_half_spectrum_open2,
                                  z_half_spectrum_open3,
                                  z_half_spectrum_open4,
                                  z_half_spectrum_dondon1,
                                  z_half_spectrum_dondon2,
                                  z_half_spectrum_dondon3,
                                  z_half_spectrum_dondon4
                                  ))
    training_labels = np.hstack((training_labels_open1,
                                 training_labels_open2,
                                 training_labels_open3,
                                 training_labels_open4,
                                 training_labels_dondon1,
                                 training_labels_dondon2,
                                 training_labels_dondon3,
                                 training_labels_dondon4
                                 ))
   
    
    
    # ここにデータとトレーニングデータを付け加える
    training = pd.DataFrame({'x':x_training_datas,
                         'y':y_training_datas,
                         'z':z_training_datas,
                         'lablel':training_labels})
#                            
#    # csvファイルに書き出し
    fileName = "fft_training.csv"
    if os.path.exists(fileName) and i==2:
        os.remove(fileName)
    training.to_csv(fileName, mode='a',header=None, index=None)
        
        
    #print('学習モデル：%s' % svm_fit)
        
    start = stop
    stop = split_second * i




# テストデータとテストラベル
start = 0 
stop = split_second
i = 1
while True:
    i += 1
    if stop > test_num:
        break
    test_open1 = open1[start : stop]
    test_open2 = open2[start : stop]
    test_open3 = open3[start : stop]
    test_open4 = open4[start : stop]

    test_dondon1 = dondon1[start : stop]
    test_dondon2 = dondon2[start : stop]
    test_dondon3 = dondon3[start : stop]
    test_dondon4 = dondon4[start : stop]

    ################################################################################
#                                   fft
################################################################################

    fs = 1000 # Sampling rate
    L = 5000 # Signal length
#NUMBER = 20


# 全部足す
#sin_open1 = training_open1
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
    half_L = int(L / 2 + 1)
    #half_L = int(L/2)
    # フーリエ変換
#    spectrum_nw_test1 = fft(sin_open1) # 窓関数なし
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
################################################################################
################################################################################

# データと同じ長さのラベルを付ける
    test_labels_open1 = np.zeros(len(x_half_spectrum_open1))
    test_labels_open2 = np.zeros(len(x_half_spectrum_open2))
    test_labels_open3 = np.zeros(len(x_half_spectrum_open3))
    test_labels_open4 = np.zeros(len(x_half_spectrum_open4))

    test_labels_dondon1 = np.ones(len(x_half_spectrum_dondon1))
    test_labels_dondon2 = np.ones(len(x_half_spectrum_dondon2))
    test_labels_dondon3 = np.ones(len(x_half_spectrum_dondon3))
    test_labels_dondon4 = np.ones(len(x_half_spectrum_dondon4))
    
    
# データ結合   
    x_test_datas = np.hstack((x_half_spectrum_open1,
                                  x_half_spectrum_open2,
                                  x_half_spectrum_open3,
                                  x_half_spectrum_open4,
                                  x_half_spectrum_dondon1,
                                  x_half_spectrum_dondon2,
                                  x_half_spectrum_dondon3,
                                  x_half_spectrum_dondon4
                                  ))
    
    y_test_datas = np.hstack((y_half_spectrum_open1,
                                  y_half_spectrum_open2,
                                  y_half_spectrum_open3,
                                  y_half_spectrum_open4,
                                  y_half_spectrum_dondon1,
                                  y_half_spectrum_dondon2,
                                  y_half_spectrum_dondon3,
                                  y_half_spectrum_dondon4
                                  ))
    
    z_test_datas = np.hstack((z_half_spectrum_open1,
                                  z_half_spectrum_open2,
                                  z_half_spectrum_open3,
                                  z_half_spectrum_open4,
                                  z_half_spectrum_dondon1,
                                  z_half_spectrum_dondon2,
                                  z_half_spectrum_dondon3,
                                  z_half_spectrum_dondon4
                                  ))
    test_labels = np.hstack((test_labels_open1,
                                 test_labels_open2,
                                 test_labels_open3,
                                 test_labels_open4,
                                 test_labels_dondon1,
                                 test_labels_dondon2,
                                 test_labels_dondon3,
                                 test_labels_dondon4
                                 ))
   
    
    
    # ここにデータとトレーニングデータを付け加える
    test = pd.DataFrame({'x':x_test_datas,
                         'y':y_test_datas,
                         'z':z_test_datas,
                         'lablel':test_labels})

                            
    # csvファイルに書き出し
    fileName = "fft_test.csv"
    if os.path.exists(fileName) and i==2:
        os.remove(fileName)
    test.to_csv(fileName, mode='a',header=None, index=None)

    
    start = stop
    stop = split_second * i












    


################################################################################
################################################################################







