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

################################################################################
################################################################################



################################################################################
#                                   SVM
################################################################################

    
# トレーニングデータとテストデータを ７:３ に分割
training_datas_quotient_num = int(quotient_min * 0.7)
test_labels_quotient_num = int(quotient_min - training_datas_quotient_num)

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

    # 最小値
    min_training_datas_open1 = training_open1.min()
    min_training_datas_open2 = training_open2.min()
    min_training_datas_open3 = training_open3.min()
    min_training_datas_open4 = training_open4.min()
    
    min_training_datas_dondon1 = training_dondon1.min()
    min_training_datas_dondon2 = training_dondon2.min()
    min_training_datas_dondon3 = training_dondon3.min()
    min_training_datas_dondon4 = training_dondon4.min()
    
    # 最大値
    max_training_datas_open1 = training_open1.max()
    max_training_datas_open2 = training_open2.max()
    max_training_datas_open3 = training_open3.max()
    max_training_datas_open4 = training_open4.max()
    
    max_training_datas_dondon1 = training_dondon1.max()
    max_training_datas_dondon2 = training_dondon2.max()
    max_training_datas_dondon3 = training_dondon3.max()
    max_training_datas_dondon4 = training_dondon4.max()
    
    # 中央値
    median_training_datas_open1 = training_open1.median()
    median_training_datas_open2 = training_open2.median()
    median_training_datas_open3 = training_open3.median()
    median_training_datas_open4 = training_open4.median()
    
    median_training_datas_dondon1 = training_dondon1.median()
    median_training_datas_dondon2 = training_dondon2.median()
    median_training_datas_dondon3 = training_dondon3.median()
    median_training_datas_dondon4 = training_dondon4.median()
    
    # 平均
    mean_training_datas_open1 = training_open1.mean()
    mean_training_datas_open2 = training_open2.mean()
    mean_training_datas_open3 = training_open3.mean()
    mean_training_datas_open4 = training_open4.mean()
    
    mean_training_datas_dondon1 = training_dondon1.mean()
    mean_training_datas_dondon2 = training_dondon2.mean()
    mean_training_datas_dondon3 = training_dondon3.mean()
    mean_training_datas_dondon4 = training_dondon4.mean()
    
    # 分散
    var_training_datas_open1 = training_open1.var(ddof=False)
    var_training_datas_open2 = training_open2.var(ddof=False)
    var_training_datas_open3 = training_open3.var(ddof=False)
    var_training_datas_open4 = training_open4.var(ddof=False)
    
    var_training_datas_dondon1 = training_dondon1.var(ddof=False)
    var_training_datas_dondon2 = training_dondon2.var(ddof=False)
    var_training_datas_dondon3 = training_dondon3.var(ddof=False)
    var_training_datas_dondon4 = training_dondon4.var(ddof=False)
    
    
    statistick_training_datas_open1 = np.hstack((min_training_datas_open1,
                                                 max_training_datas_open1,
                                                 median_training_datas_open1,
                                                 mean_training_datas_open1,
                                                 var_training_datas_open1))
    
    statistick_training_datas_open2 = np.hstack((min_training_datas_open2,
                                                 max_training_datas_open2,
                                                 median_training_datas_open2,
                                                 mean_training_datas_open2,
                                                 var_training_datas_open2))
        
    statistick_training_datas_open3 = np.vstack((min_training_datas_open3,
                                                 max_training_datas_open3,
                                                 median_training_datas_open3,
                                                 mean_training_datas_open3,
                                                 var_training_datas_open3))
            
    statistick_training_datas_open4 = np.vstack((min_training_datas_open4,
                                                 max_training_datas_open4,
                                                 median_training_datas_open4,
                                                 mean_training_datas_open4,
                                                 var_training_datas_open4))
    
    statistick_training_datas_dondon1 = np.hstack((min_training_datas_dondon1,
                                                 max_training_datas_dondon1,
                                                 median_training_datas_dondon1,
                                                 mean_training_datas_dondon1,
                                                 var_training_datas_open1))
    
    statistick_training_datas_dondon2 = np.hstack((min_training_datas_dondon2,
                                                 max_training_datas_dondon2,
                                                 median_training_datas_dondon2,
                                                 mean_training_datas_dondon2,
                                                 var_training_datas_dondon2))
    
    statistick_training_datas_dondon3 = np.vstack((min_training_datas_dondon3,
                                                 max_training_datas_dondon3,
                                                 median_training_datas_dondon3,
                                                 mean_training_datas_dondon3,
                                                 var_training_datas_dondon3))

    statistick_training_datas_dondon4 = np.vstack((min_training_datas_dondon4,
                                                 max_training_datas_dondon4,
                                                 median_training_datas_dondon4,
                                                 mean_training_datas_dondon4,
                                                 var_training_datas_dondon4))    
    
    # データ変形　x,y,z * min,max,median,mean,var    
    open1_shape = statistick_training_datas_open1.reshape(3,5)
    open2_shape = statistick_training_datas_open2.reshape(3,5)
    open3_shape = statistick_training_datas_open3.reshape(3,5)
    open4_shape = statistick_training_datas_open4.reshape(3,5)
    
    dondon1_shape = statistick_training_datas_dondon1.reshape(3,5)
    dondon2_shape = statistick_training_datas_dondon2.reshape(3,5)
    dondon3_shape = statistick_training_datas_dondon3.reshape(3,5)
    dondon4_shape = statistick_training_datas_dondon4.reshape(3,5)
    
    statistick_training_datas_open = np.vstack((open1_shape,
                                                open2_shape,
                                                open3_shape,
                                                open4_shape
                                           ))
    
    statistick_training_datas_dondon = np.vstack((dondon1_shape,
                                                  dondon2_shape,
                                                  dondon3_shape,
                                                  dondon4_shape
                                           ))
    statistick_training_datas = np.vstack((statistick_training_datas_open,
                                           statistick_training_datas_dondon))
    
    training_labels_open = np.zeros(len(statistick_training_datas_open[:,0]))
    training_labels_dondon = np.ones(len(statistick_training_datas_dondon[:,0]))
    training_labels = np.hstack((training_labels_open, training_labels_dondon))
    
     
    
    # ここにデータとトレーニングデータを付け加える
    training = pd.DataFrame({'min':statistick_training_datas[:,0],
                            'max':statistick_training_datas[:,1],
                            'median':statistick_training_datas[:,2],
                            'mean':statistick_training_datas[:,3],
                            'var':statistick_training_datas[:,4],
                            'lablel':training_labels})
                            
    # csvファイルに書き出し
    fileName = "dondon_door-open_training.csv"
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

    # 最小値
    min_test_datas_open1 = test_open1.min()
    min_test_datas_open2 = test_open2.min()
    min_test_datas_open3 = test_open3.min()
    min_test_datas_open4 = test_open4.min()

    min_test_datas_dondon1 = test_dondon1.min()
    min_test_datas_dondon2 = test_dondon2.min()
    min_test_datas_dondon3 = test_dondon3.min()
    min_test_datas_dondon4 = test_dondon4.min()
    # 最大値
    max_test_datas_open1 = test_open1.max()
    max_test_datas_open2 = test_open2.max()
    max_test_datas_open3 = test_open3.max()
    max_test_datas_open4 = test_open4.max()

    max_test_datas_dondon1 = test_dondon1.max()
    max_test_datas_dondon2 = test_dondon2.max()
    max_test_datas_dondon3 = test_dondon3.max()
    max_test_datas_dondon4 = test_dondon4.max()

    # 中央値
    median_test_datas_open1 = test_open1.median()
    median_test_datas_open2 = test_open2.median()
    median_test_datas_open3 = test_open3.median()
    median_test_datas_open4 = test_open4.median()

    median_test_datas_dondon1 = test_dondon1.median()
    median_test_datas_dondon2 = test_dondon2.median()
    median_test_datas_dondon3 = test_dondon3.median()
    median_test_datas_dondon4 = test_dondon4.median()    
    # 平均
    mean_test_datas_open1 = test_open1.mean()
    mean_test_datas_open2 = test_open2.mean()
    mean_test_datas_open3 = test_open3.mean()
    mean_test_datas_open4 = test_open4.mean()

    mean_test_datas_dondon1 = test_dondon1.mean()
    mean_test_datas_dondon2 = test_dondon2.mean()
    mean_test_datas_dondon3 = test_dondon3.mean()
    mean_test_datas_dondon4 = test_dondon4.mean()
    # 分散
    var_test_datas_open1 = test_open1.var(ddof=False)
    var_test_datas_open2 = test_open2.var(ddof=False)
    var_test_datas_open3 = test_open3.var(ddof=False)
    var_test_datas_open4 = test_open4.var(ddof=False)

    var_test_datas_dondon1 = test_dondon1.var(ddof=False)
    var_test_datas_dondon2 = test_dondon2.var(ddof=False)
    var_test_datas_dondon3 = test_dondon3.var(ddof=False)
    var_test_datas_dondon4 = test_dondon4.var(ddof=False)    
    #print(var_test_datas)
    
    statistick_test_datas_open1 = np.hstack((min_test_datas_open1,
                                             max_test_datas_open1,
                                           median_test_datas_open1,
                                           mean_test_datas_open1,
                                           var_test_datas_open1))

    statistick_test_datas_open2 = np.hstack((min_test_datas_open2,
                                             max_test_datas_open2,
                                           median_test_datas_open2,
                                           mean_test_datas_open2,
                                           var_test_datas_open2))

    statistick_test_datas_open3 = np.vstack((min_test_datas_open3,
                                             max_test_datas_open3,
                                           median_test_datas_open3,
                                           mean_test_datas_open3,
                                           var_test_datas_open3))

    statistick_test_datas_open4 = np.vstack((min_test_datas_open4,
                                             max_test_datas_open4,
                                           median_test_datas_open4,
                                           mean_test_datas_open4,
                                           var_test_datas_open4))    

    statistick_test_datas_dondon1 = np.hstack((min_test_datas_dondon1,
                                             max_test_datas_dondon1,
                                           median_test_datas_dondon1,
                                           mean_test_datas_dondon1,
                                           var_test_datas_dondon1))

    statistick_test_datas_dondon2 = np.hstack((min_test_datas_dondon2,
                                             max_test_datas_dondon2,
                                           median_test_datas_dondon2,
                                           mean_test_datas_dondon2,
                                           var_test_datas_dondon2))

    statistick_test_datas_dondon3 = np.vstack((min_test_datas_dondon3,
                                             max_test_datas_dondon3,
                                           median_test_datas_dondon3,
                                           mean_test_datas_dondon3,
                                           var_test_datas_dondon3))

    statistick_test_datas_dondon4 = np.vstack((min_test_datas_dondon4,
                                             max_test_datas_dondon4,
                                           median_test_datas_dondon4,
                                           mean_test_datas_dondon4,
                                           var_test_datas_dondon4)) 
    
    open1_shape = statistick_test_datas_open1.reshape(3,5)
    open2_shape = statistick_test_datas_open2.reshape(3,5)
    open3_shape = statistick_test_datas_open3.reshape(3,5)
    open4_shape = statistick_test_datas_open4.reshape(3,5)

    dondon1_shape = statistick_test_datas_dondon1.reshape(3,5)
    dondon2_shape = statistick_test_datas_dondon2.reshape(3,5)
    dondon3_shape = statistick_test_datas_dondon3.reshape(3,5)
    dondon4_shape = statistick_test_datas_dondon4.reshape(3,5)
    
    statistick_test_datas_open = np.vstack((open1_shape,
                                           open2_shape,
                                           open3_shape,
                                           open4_shape
                                            ))
    
    statistick_test_datas_dondon = np.vstack((dondon1_shape,
                                              dondon2_shape,
                                              dondon3_shape,
                                              dondon4_shape
                                           ))
    statistick_test_datas = np.vstack((statistick_test_datas_open,
                                           statistick_test_datas_dondon))
    # 行数分だけラベルを作成
    test_labels_open = np.zeros(len(statistick_test_datas_open[:,0]))
    test_labels_dondon = np.ones(len(statistick_test_datas_dondon[:,0]))
    test_labels = np.hstack((test_labels_open, test_labels_dondon))   
    
    training = pd.DataFrame({'min':statistick_test_datas[:,0],
                        'max':statistick_test_datas[:,1],
                        'median':statistick_test_datas[:,2],
                        'mean':statistick_test_datas[:,3],
                        'var':statistick_test_datas[:,4],
                        'labels':test_labels})
                            
    # csvファイルに書き出し
    fileName = "dondon_door-open_test.csv"
    if os.path.exists(fileName) and i==2:
        os.remove(fileName)
    training.to_csv(fileName, mode='a',header=None, index=None)

    
    start = stop
    stop = split_second * i












    


################################################################################
################################################################################







